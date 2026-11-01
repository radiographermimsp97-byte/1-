package com.example

import android.app.Activity
import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.FileProvider
import com.example.ui.theme.MyApplicationTheme
import java.io.File

class MainActivity : ComponentActivity() {
  private var fileUploadCallback: android.webkit.ValueCallback<Array<Uri>>? = null
  private val fileChooserLauncher = registerForActivityResult(
    androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult()
  ) { result ->
    val uris = if (result.resultCode == RESULT_OK) {
      val data = result.data
      if (data?.clipData != null) {
        val count = data.clipData!!.itemCount
        Array(count) { i -> data.clipData!!.getItemAt(i).uri }
      } else if (data?.data != null) {
        arrayOf(data.data!!)
      } else {
        null
      }
    } else {
      null
    }
    fileUploadCallback?.onReceiveValue(uris)
    fileUploadCallback = null
  }

  fun launchFileChooser(callback: android.webkit.ValueCallback<Array<Uri>>?) {
    fileUploadCallback?.onReceiveValue(null)
    fileUploadCallback = callback
    val intent = Intent(Intent.ACTION_GET_CONTENT).apply {
      type = "image/*"
      addCategory(Intent.CATEGORY_OPENABLE)
    }
    try {
      fileChooserLauncher.launch(intent)
    } catch (_: Exception) {
      fileUploadCallback = null
    }
  }

  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    enableEdgeToEdge()
    try {
      val webViewCacheDir = File(cacheDir, "WebView/Default/HTTP Cache/Code Cache/js")
      if (!webViewCacheDir.exists()) {
        webViewCacheDir.mkdirs()
      }
    } catch (_: Exception) {}
    WebView.setWebContentsDebuggingEnabled(true)
    setContent {
      MyApplicationTheme {
        Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
          ScoutAppScreen(
            modifier = Modifier.padding(innerPadding),
            onLaunchFileChooser = { cb -> launchFileChooser(cb) }
          )
        }
      }
    }
  }
}

class WebAppInterface(private val context: Context) {
  @JavascriptInterface
  fun generateAndSharePdf(

    title: String,
    groupName: String,
    period: String,
    totalSessions: Int,
    kpiStatsJson: String,
    tableRowsJson: String
  ): String {
    return try {
      android.os.Handler(android.os.Looper.getMainLooper()).post {
        try {
          val cleanTitle = title.replace("[^a-zA-Z0-9_.-]".toRegex(), "_")
          val pdfFile = File(context.cacheDir, "$cleanTitle.pdf")

          // Create PDF Document using Android Native android.graphics.pdf.PdfDocument
          val pdfDoc = android.graphics.pdf.PdfDocument()

          // Standard A4 dimensions in PostScript points: 595 x 842 pt
          val pageWidth = 595
          val pageHeight = 842
          var pageNumber = 1

          var pageInfo = android.graphics.pdf.PdfDocument.PageInfo.Builder(pageWidth, pageHeight, pageNumber).create()
          var page = pdfDoc.startPage(pageInfo)
          var canvas = page.canvas

          val paintText = android.graphics.Paint().apply {
            color = android.graphics.Color.BLACK
            textSize = 10f
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.RIGHT
          }

          val paintTitle = android.graphics.Paint().apply {
            color = android.graphics.Color.parseColor("#065f46")
            textSize = 15f
            isFakeBoldText = true
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }

          val paintSub = android.graphics.Paint().apply {
            color = android.graphics.Color.parseColor("#334155")
            textSize = 10f
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }

          val paintBg = android.graphics.Paint().apply {
            isAntiAlias = true
          }

          val paintBorder = android.graphics.Paint().apply {
            color = android.graphics.Color.parseColor("#cbd5e1")
            strokeWidth = 1f
            style = android.graphics.Paint.Style.STROKE
          }

          var y = 45f

          // Top Official Header
          canvas.drawText("الجمهورية الجزائرية الديمقراطية الشعبية", (pageWidth / 2).toFloat(), y, paintSub)
          y += 18f
          canvas.drawText("الكشافة الإسلامية الجزائرية - $groupName", (pageWidth / 2).toFloat(), y, paintSub)
          y += 22f
          canvas.drawText("تقرير إحصائيات حضور وغياب قادة الفوج", (pageWidth / 2).toFloat(), y, paintTitle)
          y += 16f
          canvas.drawText("الفترة: $period  |  إجمالي الحصص: $totalSessions حصة", (pageWidth / 2).toFloat(), y, paintSub)
          y += 22f

          // Draw Divider
          paintBg.color = android.graphics.Color.parseColor("#065f46")
          canvas.drawRect(40f, y, (pageWidth - 40).toFloat(), y + 2f, paintBg)
          y += 16f

          // Draw KPI Summary Box
          val kpiObj = try { org.json.JSONObject(kpiStatsJson) } catch (_: Exception) { org.json.JSONObject() }
          val rate = kpiObj.optInt("rate", 0)
          val ontime = kpiObj.optInt("ontime", 0)
          val lateExc = kpiObj.optInt("lateExcused", 0)
          val lateUnexc = kpiObj.optInt("lateUnexcused", 0)
          val absExc = kpiObj.optInt("absentExcused", 0)
          val absUnexc = kpiObj.optInt("absentUnexcused", 0)

          paintBg.color = android.graphics.Color.parseColor("#f8fafc")
          canvas.drawRoundRect(40f, y, (pageWidth - 40).toFloat(), y + 42f, 8f, 8f, paintBg)
          canvas.drawRoundRect(40f, y, (pageWidth - 40).toFloat(), y + 42f, 8f, 8f, paintBorder)

          val kpiW = (pageWidth - 80) / 6f
          val kpiItems = listOf(
            Pair("نسبة الانضباط", "$rate%"),
            Pair("في الوقت", "$ontime"),
            Pair("متأخر بعذر", "$lateExc"),
            Pair("متأخر بدون", "$lateUnexc"),
            Pair("غائب بعذر", "$absExc"),
            Pair("غائب بدون", "$absUnexc")
          )

          val paintKpiTitle = android.graphics.Paint().apply {
            color = android.graphics.Color.parseColor("#64748b")
            textSize = 8f
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }
          val paintKpiVal = android.graphics.Paint().apply {
            color = android.graphics.Color.parseColor("#0f172a")
            textSize = 11f
            isFakeBoldText = true
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }

          kpiItems.forEachIndexed { idx, pair ->
            val cx = 40f + (idx * kpiW) + (kpiW / 2f)
            canvas.drawText(pair.first, cx, y + 16f, paintKpiTitle)
            canvas.drawText(pair.second, cx, y + 33f, paintKpiVal)
          }

          y += 58f

          // Draw Table Header
          paintBg.color = android.graphics.Color.parseColor("#065f46")
          canvas.drawRect(40f, y, (pageWidth - 40).toFloat(), y + 24f, paintBg)

          val paintTh = android.graphics.Paint().apply {
            color = android.graphics.Color.WHITE
            textSize = 8.5f
            isFakeBoldText = true
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }

          val cols = listOf(
            Triple(40f, 65f, "الرقم"),
            Triple(65f, 185f, "اسم القائد"),
            Triple(185f, 265f, "الوحدة / المسؤولية"),
            Triple(265f, 305f, "في الوقت"),
            Triple(305f, 345f, "تأخر عذر"),
            Triple(345f, 385f, "تأخر بدون"),
            Triple(385f, 425f, "غياب عذر"),
            Triple(425f, 465f, "غياب بدون"),
            Triple(465f, 510f, "إجمالي الحضور"),
            Triple(510f, 555f, "الانضباط")
          )

          cols.forEach { col ->
            val cx = (col.first + col.second) / 2f
            canvas.drawText(col.third, cx, y + 15f, paintTh)
          }

          y += 24f

          // Draw Rows
          val rowsArr = try { org.json.JSONArray(tableRowsJson) } catch (_: Exception) { org.json.JSONArray() }
          val rowHeight = 22f

          val paintTdCenter = android.graphics.Paint().apply {
            color = android.graphics.Color.BLACK
            textSize = 8.5f
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }
          val paintTdRight = android.graphics.Paint().apply {
            color = android.graphics.Color.BLACK
            textSize = 8.5f
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.RIGHT
          }

          for (i in 0 until rowsArr.length()) {
            val rowObj = rowsArr.optJSONObject(i) ?: continue

            // Page break check
            if (y + rowHeight > pageHeight - 80) {
              pdfDoc.finishPage(page)
              pageNumber++
              pageInfo = android.graphics.pdf.PdfDocument.PageInfo.Builder(pageWidth, pageHeight, pageNumber).create()
              page = pdfDoc.startPage(pageInfo)
              canvas = page.canvas
              y = 40f

              // Redraw Table Header on new page
              paintBg.color = android.graphics.Color.parseColor("#065f46")
              canvas.drawRect(40f, y, (pageWidth - 40).toFloat(), y + 24f, paintBg)
              cols.forEach { col ->
                val cx = (col.first + col.second) / 2f
                canvas.drawText(col.third, cx, y + 15f, paintTh)
              }
              y += 24f
            }

            // Alternating row color
            paintBg.color = if (i % 2 == 0) android.graphics.Color.WHITE else android.graphics.Color.parseColor("#f8fafc")
            canvas.drawRect(40f, y, (pageWidth - 40).toFloat(), y + rowHeight, paintBg)
            canvas.drawLine(40f, y + rowHeight, (pageWidth - 40).toFloat(), y + rowHeight, paintBorder)

            // Cell contents
            val numStr = "${i + 1}"
            val nameStr = rowObj.optString("name", "")
            val unitStr = rowObj.optString("unit", "")
            val ontimeStr = "${rowObj.optInt("ontime", 0)}"
            val lateExcStr = "${rowObj.optInt("lateExcused", 0)}"
            val lateUnexcStr = "${rowObj.optInt("lateUnexcused", 0)}"
            val absExcStr = "${rowObj.optInt("absentExcused", 0)}"
            val absUnexcStr = "${rowObj.optInt("absentUnexcused", 0)}"
            val totPresStr = "${rowObj.optInt("totalPresent", 0)}"
            val rateStr = "${rowObj.optInt("rate", 0)}%"

            canvas.drawText(numStr, (cols[0].first + cols[0].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(nameStr, cols[1].second - 4f, y + 14f, paintTdRight)
            canvas.drawText(unitStr, (cols[2].first + cols[2].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(ontimeStr, (cols[3].first + cols[3].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(lateExcStr, (cols[4].first + cols[4].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(lateUnexcStr, (cols[5].first + cols[5].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(absExcStr, (cols[6].first + cols[6].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(absUnexcStr, (cols[7].first + cols[7].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(totPresStr, (cols[8].first + cols[8].second) / 2f, y + 14f, paintTdCenter)
            canvas.drawText(rateStr, (cols[9].first + cols[9].second) / 2f, y + 14f, paintTdCenter)

            y += rowHeight
          }

          // Signatures section at bottom
          if (y + 70f > pageHeight - 30) {
            pdfDoc.finishPage(page)
            pageNumber++
            pageInfo = android.graphics.pdf.PdfDocument.PageInfo.Builder(pageWidth, pageHeight, pageNumber).create()
            page = pdfDoc.startPage(pageInfo)
            canvas = page.canvas
            y = 40f
          }

          y += 25f
          paintBg.color = android.graphics.Color.parseColor("#0f172a")
          canvas.drawRect(40f, y, (pageWidth - 40).toFloat(), y + 1f, paintBg)
          y += 18f

          val paintSign = android.graphics.Paint().apply {
            color = android.graphics.Color.parseColor("#1e293b")
            textSize = 9.5f
            isFakeBoldText = true
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }
          val paintSignSub = android.graphics.Paint().apply {
            color = android.graphics.Color.parseColor("#64748b")
            textSize = 8f
            isAntiAlias = true
            textAlign = android.graphics.Paint.Align.CENTER
          }

          val leftSignX = 140f
          val rightSignX = (pageWidth - 140).toFloat()

          canvas.drawText("مسؤول الإدارة والتنظيم", rightSignX, y, paintSign)
          canvas.drawText("التوقيع والختم: ....................", rightSignX, y + 26f, paintSignSub)

          canvas.drawText("قائد الفوج الكشفي / المشرف العام", leftSignX, y, paintSign)
          canvas.drawText("التوقيع والختم: ....................", leftSignX, y + 26f, paintSignSub)

          pdfDoc.finishPage(page)

          // Write bytes to PDF file
          java.io.FileOutputStream(pdfFile).use { out ->
            pdfDoc.writeTo(out)
          }
          pdfDoc.close()

          // Share PDF File via Intent Chooser
          val fileUri = FileProvider.getUriForFile(
            context,
            "${context.packageName}.fileprovider",
            pdfFile
          )

          val shareIntent = Intent(Intent.ACTION_SEND).apply {
            type = "application/pdf"
            putExtra(Intent.EXTRA_STREAM, fileUri)
            putExtra(Intent.EXTRA_SUBJECT, "$title.pdf")
            putExtra(Intent.EXTRA_TEXT, "مرفق تقرير قادة الفوج بصيغة PDF: $title")
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
          }

          val chooser = Intent.createChooser(shareIntent, "فتح أو حفظ تقرير PDF ($title)").apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
          }
          context.startActivity(chooser)
          showNativeToast("تم إنشاء وتصدير ملف الـ PDF بنجاح 📄")
        } catch (innerEx: Exception) {
          innerEx.printStackTrace()
          showNativeToast("خطأ في توليد PDF: ${innerEx.localizedMessage}")
        }
      }
      "SUCCESS"
    } catch (e: Exception) {
      e.printStackTrace()
      "ERR: " + e.localizedMessage
    }
  }

  @JavascriptInterface
  fun saveBase64PdfAndShare(fileName: String, base64Pdf: String): String {
    return try {
      val cleanName = fileName.replace("[^a-zA-Z0-9_.-]".toRegex(), "_")
      val outFile = File(context.cacheDir, if (cleanName.endsWith(".pdf")) cleanName else "$cleanName.pdf")
      val cleanBase64 = if (base64Pdf.contains(",")) base64Pdf.substringAfter(",") else base64Pdf
      val bytes = android.util.Base64.decode(cleanBase64, android.util.Base64.DEFAULT)
      outFile.writeBytes(bytes)
      val fileUri: Uri = FileProvider.getUriForFile(
        context,
        "${context.packageName}.fileprovider",
        outFile
      )
      val shareIntent = Intent(Intent.ACTION_SEND).apply {
        type = "application/pdf"
        putExtra(Intent.EXTRA_STREAM, fileUri)
        putExtra(Intent.EXTRA_SUBJECT, fileName)
        putExtra(Intent.EXTRA_TEXT, "ملف التقرير الكشفي المرفق: $fileName")
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      val chooser = Intent.createChooser(shareIntent, "مشاركة / فتح ملف PDF ($fileName)").apply {
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      context.startActivity(chooser)
      showNativeToast("تم حفظ ومشاركة ملف الـ PDF بنجاح 📄")
      "SUCCESS"
    } catch (e: Exception) {
      e.printStackTrace()
      "ERR: " + e.localizedMessage
    }
  }

  @JavascriptInterface
  fun printCurrentPage() {
    try {
      android.os.Handler(android.os.Looper.getMainLooper()).post {
        val printManager = context.getSystemService(Context.PRINT_SERVICE) as? android.print.PrintManager
        if (printManager != null) {
          // Find WebView in the current activity
          if (context is Activity) {
            val webView = context.findViewById<WebView>(android.R.id.content)?.findViewWithTag<WebView>("MainScoutWebView")
              ?: findWebView(context.window.decorView)
            if (webView != null) {
              val printAdapter = webView.createPrintDocumentAdapter("Scout_Leaders_Report")
              val jobName = "تقرير حضور وغياب قادة الفوج"
              printManager.print(jobName, printAdapter, android.print.PrintAttributes.Builder().build())
            } else {
              showNativeToast("جاري تجهيز وثيقة الطباعة...")
            }
          }
        } else {
          showNativeToast("خدمة الطباعة وحفظ PDF غير مدعومة على هذا الجهاز")
        }
      }
    } catch (e: Exception) {
      e.printStackTrace()
      showNativeToast("تعذر فتح مدير الطباعة: ${e.localizedMessage}")
    }
  }

  @JavascriptInterface
  fun saveAndShareHtmlReport(fileName: String, htmlContent: String): String {
    return try {
      val cleanName = fileName.replace("[^a-zA-Z0-9_.-]".toRegex(), "_")
      val outFile = File(context.cacheDir, if (cleanName.endsWith(".html")) cleanName else "$cleanName.html")
      outFile.writeText(htmlContent, Charsets.UTF_8)
      val fileUri: Uri = FileProvider.getUriForFile(
        context,
        "${context.packageName}.fileprovider",
        outFile
      )
      val shareIntent = Intent(Intent.ACTION_SEND).apply {
        type = "text/html"
        putExtra(Intent.EXTRA_STREAM, fileUri)
        putExtra(Intent.EXTRA_SUBJECT, fileName)
        putExtra(Intent.EXTRA_TEXT, "تقرير إحصائيات قادة الفوج: $fileName")
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      val chooser = Intent.createChooser(shareIntent, "مشاركة / طباعة تقرير القادة ($fileName)").apply {
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      context.startActivity(chooser)
      showNativeToast("تم تجهيز التقرير للمشاركة والطباعة بنجاح 📄")
      "SUCCESS"
    } catch (e: Exception) {
      e.printStackTrace()
      "ERR: " + e.localizedMessage
    }
  }

  private val prefs by lazy {
    context.getSharedPreferences("scout_native_storage", Context.MODE_PRIVATE)
  }

  @JavascriptInterface
  fun isAndroidNative(): Boolean = true

  @JavascriptInterface
  fun getStorageItem(key: String): String? {
    return if (prefs.contains(key)) prefs.getString(key, null) else null
  }

  @JavascriptInterface
  fun setStorageItem(key: String, value: String) {
    try {
      prefs.edit().putString(key, value).apply()
    } catch (_: Exception) {}
  }

  @JavascriptInterface
  fun removeStorageItem(key: String) {
    try {
      prefs.edit().remove(key).apply()
    } catch (_: Exception) {}
  }

  @JavascriptInterface
  fun clearStorage() {
    try {
      prefs.edit().clear().apply()
    } catch (_: Exception) {}
  }

  @JavascriptInterface
  fun getAllStorageKeys(): String {
    return try {
      val keys = prefs.all.keys
      val jsonArray = org.json.JSONArray()
      keys.forEach { jsonArray.put(it) }
      jsonArray.toString()
    } catch (_: Exception) {
      "[]"
    }
  }

  @JavascriptInterface
  fun getOfflineResourcesStatus(): String {
    return try {
      val appInfo = context.applicationInfo
      val apkFile = File(appInfo.sourceDir)
      val apkSizeMb = if (apkFile.exists()) apkFile.length() / (1024 * 1024) else 0
      val cacheDir = context.cacheDir
      val cacheSizeKb = cacheDir.walkTopDown().filter { it.isFile }.map { it.length() }.sum() / 1024

      """{
        "bundledLibs": true,
        "offlineReady": true,
        "apkSizeMb": $apkSizeMb,
        "cacheSizeKb": $cacheSizeKb,
        "package": "${context.packageName}",
        "status": "ALL_LIBRARIES_BUNDLED_AND_CACHED"
      }""".trimIndent()
    } catch (e: Exception) {
      """{"bundledLibs": true, "offlineReady": true, "error": "${e.message}"}"""
    }
  }

  @JavascriptInterface
  fun showNativeToast(message: String) {
    try {
      android.os.Handler(android.os.Looper.getMainLooper()).post {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
      }
    } catch (_: Exception) {}
  }

  @JavascriptInterface
  fun shareApkFile(): String {
    return try {
      val appInfo = context.applicationInfo
      val sourceApk = File(appInfo.sourceDir)
      if (!sourceApk.exists()) {
        return "ERR_SOURCE_NOT_FOUND"
      }

      val cacheApk = File(context.cacheDir, "ElFawj_ElRaqami.apk")
      sourceApk.copyTo(cacheApk, overwrite = true)

      val apkUri: Uri = FileProvider.getUriForFile(
        context,
        "${context.packageName}.fileprovider",
        cacheApk
      )

      val shareIntent = Intent(Intent.ACTION_SEND).apply {
        type = "application/vnd.android.package-archive"
        putExtra(Intent.EXTRA_STREAM, apkUri)
        putExtra(Intent.EXTRA_SUBJECT, "تطبيق الفوج الرقمي (APK)")
        putExtra(
          Intent.EXTRA_TEXT,
          "تطبيق الفوج الرقمي للكشافة الإسلامية الجزائرية 🇩🇿\nانقر على ملف الـ APK المرفق لتثبيت التطبيق مباشرة على هاتفك."
        )
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }

      val chooser = Intent.createChooser(shareIntent, "مشاركة ملف تطبيق الفوج الرقمي (APK)").apply {
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      context.startActivity(chooser)
      "SUCCESS"
    } catch (e: Exception) {
      e.printStackTrace()
      "ERR: " + e.localizedMessage
    }
  }

  @JavascriptInterface
  fun shareLink(title: String, message: String, url: String) {
    try {
      val fullText = "$title\n\n$message\n$url"
      val intent = Intent(Intent.ACTION_SEND).apply {
        type = "text/plain"
        putExtra(Intent.EXTRA_SUBJECT, title)
        putExtra(Intent.EXTRA_TEXT, fullText)
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      val chooser = Intent.createChooser(intent, title).apply {
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      context.startActivity(chooser)
    } catch (e: Exception) {
      e.printStackTrace()
    }
  }

  @JavascriptInterface
  fun saveCustomAppIcon(base64Data: String): Boolean {
    return try {
      val iconFile = File(context.filesDir, "custom_app_icon.png")
      val cleanData = if (base64Data.contains(",")) base64Data.substringAfter(",") else base64Data
      val bytes = android.util.Base64.decode(cleanData, android.util.Base64.DEFAULT)
      iconFile.writeBytes(bytes)
      showNativeToast("تم حفظ وتحديث أيقونة التطبيق بنجاح ⚜️")
      true
    } catch (e: Exception) {
      e.printStackTrace()
      false
    }
  }

  @JavascriptInterface
  fun getSavedCustomAppIcon(): String {
    return try {
      val iconFile = File(context.filesDir, "custom_app_icon.png")
      if (iconFile.exists()) {
        val bytes = iconFile.readBytes()
        "data:image/png;base64," + android.util.Base64.encodeToString(bytes, android.util.Base64.NO_WRAP)
      } else {
        ""
      }
    } catch (e: Exception) {
      ""
    }
  }

  @JavascriptInterface
  fun saveAndShareSpreadsheet(fileName: String, base64Content: String, mimeType: String): String {
    return try {
      val cleanName = fileName.replace("[^a-zA-Z0-9_.-]".toRegex(), "_")
      val outFile = File(context.cacheDir, cleanName)
      val cleanBase64 = if (base64Content.contains(",")) base64Content.substringAfter(",") else base64Content
      val bytes = android.util.Base64.decode(cleanBase64, android.util.Base64.DEFAULT)
      outFile.writeBytes(bytes)

      val fileUri: Uri = FileProvider.getUriForFile(
        context,
        "${context.packageName}.fileprovider",
        outFile
      )

      val shareIntent = Intent(Intent.ACTION_SEND).apply {
        type = if (mimeType.isNotBlank()) mimeType else "text/csv"
        putExtra(Intent.EXTRA_STREAM, fileUri)
        putExtra(Intent.EXTRA_SUBJECT, fileName)
        putExtra(Intent.EXTRA_TEXT, "ملف قائمة الفتية الكشفية المرفق: $fileName")
        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      val chooser = Intent.createChooser(shareIntent, "مشاركة / فتح ملف إكسل ($fileName)").apply {
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
      }
      context.startActivity(chooser)
      showNativeToast("تم تجهيز ومشاركة ملف الإكسل بنجاح 📊")
      "SUCCESS"
    } catch (e: Exception) {
      e.printStackTrace()
      "ERR: " + e.localizedMessage
    }
  }
}

@SuppressLint("SetJavaScriptEnabled")

private fun findWebView(view: android.view.View): WebView? {
  if (view is WebView) return view
  if (view is ViewGroup) {
    for (i in 0 until view.childCount) {
      val child = findWebView(view.getChildAt(i))
      if (child != null) return child
    }
  }
  return null
}

@Composable
fun ScoutAppScreen(
  modifier: Modifier = Modifier,
  onLaunchFileChooser: ((android.webkit.ValueCallback<Array<Uri>>?) -> Unit)? = null
) {
  AndroidView(
    modifier = modifier.fillMaxSize(),
    factory = { context ->
      WebView(context).apply {
        tag = "MainScoutWebView"

        layoutParams = ViewGroup.LayoutParams(
          ViewGroup.LayoutParams.MATCH_PARENT,
          ViewGroup.LayoutParams.MATCH_PARENT
        )
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as? ConnectivityManager
        val isConnected = try {
          val net = cm?.activeNetwork
          val caps = cm?.getNetworkCapabilities(net)
          caps?.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) == true
        } catch (_: Exception) {
          true
        }

        // Use hardware acceleration and dark background to prevent blank/black screens in emulator
        setBackgroundColor(android.graphics.Color.parseColor("#020617"))

        settings.apply {
          javaScriptEnabled = true
          domStorageEnabled = true
          allowFileAccess = true
          databaseEnabled = true
          cacheMode = WebSettings.LOAD_DEFAULT
          useWideViewPort = true
          loadWithOverviewMode = true
          setSupportZoom(false)
          allowFileAccessFromFileURLs = true
          allowUniversalAccessFromFileURLs = true
          mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        }
        addJavascriptInterface(WebAppInterface(context), "AndroidBridge")
        webChromeClient = object : WebChromeClient() {
          override fun onShowFileChooser(
            webView: WebView?,
            filePathCallback: android.webkit.ValueCallback<Array<Uri>>?,
            fileChooserParams: FileChooserParams?
          ): Boolean {
            return if (onLaunchFileChooser != null) {
              onLaunchFileChooser(filePathCallback)
              true
            } else {
              super.onShowFileChooser(webView, filePathCallback, fileChooserParams)
            }
          }

          override fun onConsoleMessage(consoleMessage: android.webkit.ConsoleMessage?): Boolean {
            android.util.Log.d("ScoutApp", "${consoleMessage?.message()} [line: ${consoleMessage?.lineNumber()}]")
            return true
          }

          override fun onJsAlert(
            view: WebView?,
            url: String?,
            message: String?,
            result: android.webkit.JsResult?
          ): Boolean {
            Toast.makeText(context, message ?: "", Toast.LENGTH_SHORT).show()
            result?.confirm()
            return true
          }

          override fun onJsConfirm(
            view: WebView?,
            url: String?,
            message: String?,
            result: android.webkit.JsResult?
          ): Boolean {
            result?.confirm()
            return true
          }
        }
        webViewClient = object : WebViewClient() {
          override fun shouldOverrideUrlLoading(view: WebView?, request: android.webkit.WebResourceRequest?): Boolean {
            val uri = request?.url ?: return false
            val url = uri.toString()
            if (url.startsWith("https://wa.me/") || url.startsWith("whatsapp://") || url.startsWith("tel:") || url.startsWith("mailto:")) {
              try {
                val intent = Intent(Intent.ACTION_VIEW, uri).apply {
                  addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                context.startActivity(intent)
                return true
              } catch (_: Exception) {}
            }
            return false
          }

          @Deprecated("Deprecated in Java")
          override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
            if (url == null) return false
            if (url.startsWith("https://wa.me/") || url.startsWith("whatsapp://") || url.startsWith("tel:") || url.startsWith("mailto:")) {
              try {
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url)).apply {
                  addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                context.startActivity(intent)
                return true
              } catch (e: Exception) {
                // Ignore if app not installed
              }
            }
            return false
          }

          override fun onReceivedError(
            view: WebView?,
            request: android.webkit.WebResourceRequest?,
            error: android.webkit.WebResourceError?
          ) {
            super.onReceivedError(view, request, error)
            android.util.Log.e("ScoutApp", "WebView resource error: ${error?.description} for ${request?.url}")
          }

          override fun onRenderProcessGone(view: WebView?, detail: android.webkit.RenderProcessGoneDetail?): Boolean {
            android.util.Log.e("ScoutApp", "WebView render process gone, reloading...")
            view?.loadUrl("file:///android_asset/index.html")
            return true
          }
        }
        loadUrl("file:///android_asset/index.html")
      }
    }
  )
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
  Text(text = "Hello $name!", modifier = modifier)
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
  MyApplicationTheme { Greeting("Android") }
}
