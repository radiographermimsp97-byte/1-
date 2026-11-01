with open("app/src/main/assets/app.source.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add all direct helper functions: saveCurriculum, saveScoutAttendance, saveLeaderAttendance, saveAnnualPlan, saveBadgeAwards
old_helpers = """const saveScouts = (newList, actionDesc = null) => {
        setScouts(newList);
        const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
        try {
          localStorage.setItem(`scout_roster_${groupCode}`, JSON.stringify(newList));
          localStorage.setItem(`scout_roster_${activeTroop}`, JSON.stringify(newList));
          localStorage.setItem("scout_roster_backup", JSON.stringify(newList));
        } catch(e) {}
        // Direct atomic cloud push to Firebase RTDB for scouts to guarantee zero loss
        try {
          const cloudUrl = normalizeCloudUrl(cloudDbUrl || localStorage.getItem("scout_cloud_url") || OFFICIAL_FIREBASE_URL);
          if (cloudUrl) {
            const cleanUrl = cloudUrl.replace(/\\/+$/, "");
            const room = sanitizeKey(activeTroop);
            fetch(`${cleanUrl}/scout_groups/${room}/scouts.json`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(newList)
            }).catch(err => console.log("Direct scouts cloud save note:", err));
          }
        } catch(err) {}
        pushToCloud({ scouts: newList });
      };"""

new_helpers = """const saveScouts = (newList, actionDesc = null) => {
        setScouts(newList);
        const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
        try {
          localStorage.setItem(`scout_roster_${groupCode}`, JSON.stringify(newList));
          localStorage.setItem(`scout_roster_${activeTroop}`, JSON.stringify(newList));
          localStorage.setItem("scout_roster_backup", JSON.stringify(newList));
        } catch(e) {}
        try {
          const cloudUrl = normalizeCloudUrl(cloudDbUrl || localStorage.getItem("scout_cloud_url") || OFFICIAL_FIREBASE_URL);
          if (cloudUrl) {
            const cleanUrl = cloudUrl.replace(/\\/+$/, "");
            const room = sanitizeKey(activeTroop);
            fetch(`${cleanUrl}/scout_groups/${room}/scouts.json`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(newList)
            }).catch(err => console.log("Direct scouts cloud save note:", err));
          }
        } catch(err) {}
        pushToCloud({ scouts: newList });
      };

      const saveCurriculum = (newList) => {
        setCurriculum(newList);
        const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
        try {
          localStorage.setItem(`scout_curriculum_${groupCode}`, JSON.stringify(newList));
          localStorage.setItem(`scout_curriculum_${activeTroop}`, JSON.stringify(newList));
          localStorage.setItem("scout_curriculum_backup", JSON.stringify(newList));
        } catch(e) {}
        try {
          const cloudUrl = normalizeCloudUrl(cloudDbUrl || localStorage.getItem("scout_cloud_url") || OFFICIAL_FIREBASE_URL);
          if (cloudUrl) {
            const cleanUrl = cloudUrl.replace(/\\/+$/, "");
            const room = sanitizeKey(activeTroop);
            fetch(`${cleanUrl}/scout_groups/${room}/curriculum.json`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(newList)
            }).catch(err => console.log("Direct curriculum cloud save note:", err));
          }
        } catch(err) {}
        pushToCloud({ curriculum: newList });
      };

      const saveScoutAttendance = (newHistory) => {
        setScoutAttendanceHistory(newHistory);
        const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
        try {
          localStorage.setItem(`scout_att_history_${groupCode}`, JSON.stringify(newHistory));
          localStorage.setItem(`scout_att_history_${activeTroop}`, JSON.stringify(newHistory));
          localStorage.setItem("scout_att_history_backup", JSON.stringify(newHistory));
        } catch(e) {}
        try {
          const cloudUrl = normalizeCloudUrl(cloudDbUrl || localStorage.getItem("scout_cloud_url") || OFFICIAL_FIREBASE_URL);
          if (cloudUrl) {
            const cleanUrl = cloudUrl.replace(/\\/+$/, "");
            const room = sanitizeKey(activeTroop);
            fetch(`${cleanUrl}/scout_groups/${room}/scoutAttendanceHistory.json`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(newHistory)
            }).catch(err => console.log("Direct scout attendance cloud save note:", err));
          }
        } catch(err) {}
        pushToCloud({ scoutAttendanceHistory: newHistory });
      };

      const saveLeaderAttendance = (newHistory) => {
        setLeaderAttendanceHistory(newHistory);
        const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
        try {
          localStorage.setItem(`scout_leader_att_history_${groupCode}`, JSON.stringify(newHistory));
          localStorage.setItem(`scout_leader_att_history_${activeTroop}`, JSON.stringify(newHistory));
          localStorage.setItem("scout_leader_att_history_backup", JSON.stringify(newHistory));
        } catch(e) {}
        try {
          const cloudUrl = normalizeCloudUrl(cloudDbUrl || localStorage.getItem("scout_cloud_url") || OFFICIAL_FIREBASE_URL);
          if (cloudUrl) {
            const cleanUrl = cloudUrl.replace(/\\/+$/, "");
            const room = sanitizeKey(activeTroop);
            fetch(`${cleanUrl}/scout_groups/${room}/leaderAttendanceHistory.json`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(newHistory)
            }).catch(err => console.log("Direct leader attendance cloud save note:", err));
          }
        } catch(err) {}
        pushToCloud({ leaderAttendanceHistory: newHistory });
      };

      const saveAnnualPlan = (newList) => {
        setAnnualPlan(newList);
        const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
        try {
          localStorage.setItem(`scout_plan_${groupCode}`, JSON.stringify(newList));
          localStorage.setItem(`scout_plan_${activeTroop}`, JSON.stringify(newList));
          localStorage.setItem("scout_plan_backup", JSON.stringify(newList));
        } catch(e) {}
        try {
          const cloudUrl = normalizeCloudUrl(cloudDbUrl || localStorage.getItem("scout_cloud_url") || OFFICIAL_FIREBASE_URL);
          if (cloudUrl) {
            const cleanUrl = cloudUrl.replace(/\\/+$/, "");
            const room = sanitizeKey(activeTroop);
            fetch(`${cleanUrl}/scout_groups/${room}/annualPlan.json`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(newList)
            }).catch(err => console.log("Direct annual plan cloud save note:", err));
          }
        } catch(err) {}
        pushToCloud({ annualPlan: newList });
      };

      const saveBadgeAwards = (newList) => {
        setBadgeAwards(newList);
        const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
        try {
          localStorage.setItem(`scout_badge_awards_${groupCode}`, JSON.stringify(newList));
          localStorage.setItem(`scout_badge_awards_${activeTroop}`, JSON.stringify(newList));
          localStorage.setItem("scout_badge_awards_backup", JSON.stringify(newList));
        } catch(e) {}
        try {
          const cloudUrl = normalizeCloudUrl(cloudDbUrl || localStorage.getItem("scout_cloud_url") || OFFICIAL_FIREBASE_URL);
          if (cloudUrl) {
            const cleanUrl = cloudUrl.replace(/\\/+$/, "");
            const room = sanitizeKey(activeTroop);
            fetch(`${cleanUrl}/scout_groups/${room}/badgeAwards.json`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(newList)
            }).catch(err => console.log("Direct badge awards cloud save note:", err));
          }
        } catch(err) {}
        pushToCloud({ badgeAwards: newList });
      };"""

assert old_helpers in text, "Error: old_helpers not found"
text = text.replace(old_helpers, new_helpers, 1)

# 2. Update pushToCloud to merge and fallback all entities from localStorage
old_push_mid = """// If currentBadges wasn't overridden directly, read latest from localStorage as fallback
        if (!overrideBadges) {
          try {
            const savedBadges = localStorage.getItem(`scout_badge_awards_${groupCode}`);
            if (savedBadges) currentBadges = JSON.parse(savedBadges);
          } catch (e) {}
        }"""

new_push_mid = """// Ensure curriculum is never overridden by stale state; read latest from localStorage if not explicitly overridden
        if (!overrideCurriculum && (!overrideScouts || typeof overrideScouts !== "object" || !overrideScouts.curriculum)) {
          try {
            const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
            const savedCurr = localStorage.getItem(`scout_curriculum_${activeTroop}`) ||
                              localStorage.getItem(`scout_curriculum_${groupCode}`);
            if (savedCurr) {
              const parsed = JSON.parse(savedCurr);
              if (Array.isArray(parsed) && parsed.length > 0) currentCurriculum = parsed;
            }
          } catch(e) {}
        }

        // Ensure annualPlan is never overridden by stale state; merge with latest from localStorage
        if (!overridePlan && (!overrideScouts || typeof overrideScouts !== "object" || !overrideScouts.annualPlan)) {
          try {
            const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
            const savedPlan = localStorage.getItem(`scout_plan_${activeTroop}`) ||
                              localStorage.getItem(`scout_plan_${groupCode}`);
            if (savedPlan) {
              const parsed = JSON.parse(savedPlan);
              if (Array.isArray(parsed) && parsed.length > 0) {
                const map = new Map();
                currentPlan.forEach(p => { if (p && p.id) map.set(p.id, p); });
                parsed.forEach(p => { if (p && p.id && !map.has(p.id)) map.set(p.id, p); });
                currentPlan = Array.from(map.values());
              }
            }
          } catch(e) {}
        }

        // Ensure badgeAwards is never overridden by stale state; merge with latest from localStorage
        if (!overrideBadges && (!overrideScouts || typeof overrideScouts !== "object" || !overrideScouts.badgeAwards)) {
          try {
            const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
            const savedBadges = localStorage.getItem(`scout_badge_awards_${activeTroop}`) ||
                                localStorage.getItem(`scout_badge_awards_${groupCode}`);
            if (savedBadges) {
              const parsed = JSON.parse(savedBadges);
              if (Array.isArray(parsed) && parsed.length > 0) {
                const map = new Map();
                currentBadges.forEach(b => { if (b && b.id) map.set(b.id, b); });
                parsed.forEach(b => { if (b && b.id && !map.has(b.id)) map.set(b.id, b); });
                currentBadges = Array.from(map.values());
              }
            }
          } catch (e) {}
        }

        // Ensure scout & leader attendance histories are preserved from localStorage
        let currentScoutAtt = scoutAttendanceHistory;
        let currentLdrAtt = leaderAttendanceHistory;
        if (overrideScouts && typeof overrideScouts === "object" && !Array.isArray(overrideScouts)) {
          if (overrideScouts.scoutAttendanceHistory) currentScoutAtt = overrideScouts.scoutAttendanceHistory;
          if (overrideScouts.leaderAttendanceHistory) currentLdrAtt = overrideScouts.leaderAttendanceHistory;
        }
        try {
          const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
          const savedScoutAtt = localStorage.getItem(`scout_att_history_${activeTroop}`) || localStorage.getItem(`scout_att_history_${groupCode}`);
          if (savedScoutAtt) {
            const parsed = JSON.parse(savedScoutAtt);
            if (parsed && typeof parsed === "object") {
              currentScoutAtt = { ...(currentScoutAtt || {}), ...parsed };
            }
          }
          const savedLdrAtt = localStorage.getItem(`scout_leader_att_history_${activeTroop}`) || localStorage.getItem(`scout_leader_att_history_${groupCode}`);
          if (savedLdrAtt) {
            const parsed = JSON.parse(savedLdrAtt);
            if (parsed && typeof parsed === "object") {
              currentLdrAtt = { ...(currentLdrAtt || {}), ...parsed };
            }
          }
        } catch(e) {}"""

assert old_push_mid in text, "Error: old_push_mid not found"
text = text.replace(old_push_mid, new_push_mid, 1)

# 2b. In payload construction, use currentScoutAtt and currentLdrAtt
old_payload = """scoutAttendanceHistory,
          leaderAttendanceHistory,"""
new_payload = """scoutAttendanceHistory: currentScoutAtt,
          leaderAttendanceHistory: currentLdrAtt,"""
assert old_payload in text, "Error: old_payload not found"
text = text.replace(old_payload, new_payload, 1)

# 2c. Save all payload items to localStorage for both activeTroop and groupCode
old_payload_saves = """try {
          const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
          localStorage.setItem(`scout_roster_${activeTroop}`, JSON.stringify(payload.scouts));
          localStorage.setItem(`scout_roster_${groupCode}`, JSON.stringify(payload.scouts));
          localStorage.setItem(`scout_plan_${groupCode}`, JSON.stringify(payload.annualPlan));
          localStorage.setItem(`scout_leaders_${groupCode}`, JSON.stringify(payload.leadersTracking));
          localStorage.setItem(`scout_curriculum_${groupCode}`, JSON.stringify(payload.curriculum));
          localStorage.setItem(`scout_notifications_${groupCode}`, JSON.stringify(payload.notifications || []));
          localStorage.setItem(`scout_badge_awards_${groupCode}`, JSON.stringify(payload.badgeAwards || []));
          localStorage.setItem(`scout_supervisors_${groupCode}`, JSON.stringify(payload.supervisorAccounts || []));
          localStorage.setItem(`scout_account_limits_${groupCode}`, JSON.stringify(payload.accountLimits || defaultAccountLimits));
          localStorage.setItem(`scout_troop_units_${groupCode}`, JSON.stringify(payload.troopUnits || []));
          localStorage.setItem(`scout_att_history_${groupCode}`, JSON.stringify(payload.scoutAttendanceHistory || {}));
          localStorage.setItem(`scout_leader_att_history_${groupCode}`, JSON.stringify(payload.leaderAttendanceHistory || {}));
        } catch (e) {}"""

new_payload_saves = """try {
          const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
          [activeTroop, groupCode].forEach(k => {
            if (!k) return;
            localStorage.setItem(`scout_roster_${k}`, JSON.stringify(payload.scouts));
            localStorage.setItem(`scout_plan_${k}`, JSON.stringify(payload.annualPlan));
            localStorage.setItem(`scout_leaders_${k}`, JSON.stringify(payload.leadersTracking));
            localStorage.setItem(`scout_curriculum_${k}`, JSON.stringify(payload.curriculum));
            localStorage.setItem(`scout_notifications_${k}`, JSON.stringify(payload.notifications || []));
            localStorage.setItem(`scout_badge_awards_${k}`, JSON.stringify(payload.badgeAwards || []));
            localStorage.setItem(`scout_supervisors_${k}`, JSON.stringify(payload.supervisorAccounts || []));
            localStorage.setItem(`scout_account_limits_${k}`, JSON.stringify(payload.accountLimits || defaultAccountLimits));
            localStorage.setItem(`scout_troop_units_${k}`, JSON.stringify(payload.troopUnits || []));
            localStorage.setItem(`scout_att_history_${k}`, JSON.stringify(payload.scoutAttendanceHistory || {}));
            localStorage.setItem(`scout_leader_att_history_${k}`, JSON.stringify(payload.leaderAttendanceHistory || {}));
          });
        } catch (e) {}"""

assert old_payload_saves in text, "Error: old_payload_saves not found"
text = text.replace(old_payload_saves, new_payload_saves, 1)

# 3. Dynamic replacement of old_pull_body
s1 = text.find("if (Array.isArray(remote.annualPlan)) setAnnualPlan(remote.annualPlan);")
s2 = text.find("if (remote.leaderAttendanceHistory) setLeaderAttendanceHistory(remote.leaderAttendanceHistory);")
assert s1 != -1 and s2 != -1, "Error: pull_body start/end not found"
end_s2 = s2 + len("if (remote.leaderAttendanceHistory) setLeaderAttendanceHistory(remote.leaderAttendanceHistory);")
old_pull_body_exact = text[s1:end_s2]

new_pull_body = """// Annual plan merge
                if (Array.isArray(remote.annualPlan)) {
                  let mergedPlan = remote.annualPlan;
                  try {
                    const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                    const saved = localStorage.getItem(`scout_plan_${activeTroop}`) || localStorage.getItem(`scout_plan_${groupCode}`);
                    if (saved) {
                      const parsed = JSON.parse(saved);
                      if (Array.isArray(parsed) && parsed.length > 0) {
                        const map = new Map();
                        remote.annualPlan.forEach(p => { if (p && p.id) map.set(p.id, p); });
                        parsed.forEach(p => { if (p && p.id && !map.has(p.id)) map.set(p.id, p); });
                        mergedPlan = Array.from(map.values());
                      }
                    }
                  } catch(e) {}
                  setAnnualPlan(mergedPlan);
                  const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                  localStorage.setItem(`scout_plan_${activeTroop}`, JSON.stringify(mergedPlan));
                  localStorage.setItem(`scout_plan_${groupCode}`, JSON.stringify(mergedPlan));
                }

                // Leaders tracking merge
                if (Array.isArray(remote.leadersTracking)) {
                  let mergedLeaders = remote.leadersTracking;
                  try {
                    const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                    const localSaved = localStorage.getItem(`scout_leaders_${activeTroop}`) || localStorage.getItem(`scout_leaders_${groupCode}`);
                    if (localSaved) {
                      const parsedLocal = JSON.parse(localSaved);
                      if (Array.isArray(parsedLocal) && parsedLocal.length > 0) {
                        const map = new Map();
                        remote.leadersTracking.forEach(l => { if (l && l.id) map.set(l.id, l); });
                        parsedLocal.forEach(l => { if (l && l.id && !map.has(l.id)) map.set(l.id, l); });
                        mergedLeaders = Array.from(map.values());
                      }
                    }
                  } catch(e) {}
                  setLeadersTracking(mergedLeaders);
                  const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                  localStorage.setItem(`scout_leaders_${activeTroop}`, JSON.stringify(mergedLeaders));
                  localStorage.setItem(`scout_leaders_${groupCode}`, JSON.stringify(mergedLeaders));
                }

                // Curriculum merge & protect
                if (Array.isArray(remote.curriculum) && remote.curriculum.length > 0) {
                  setCurriculum(remote.curriculum);
                  const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                  localStorage.setItem(`scout_curriculum_${activeTroop}`, JSON.stringify(remote.curriculum));
                  localStorage.setItem(`scout_curriculum_${groupCode}`, JSON.stringify(remote.curriculum));
                } else {
                  try {
                    const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                    const savedCurr = localStorage.getItem(`scout_curriculum_${activeTroop}`) || localStorage.getItem(`scout_curriculum_${groupCode}`);
                    if (savedCurr) {
                      const parsed = JSON.parse(savedCurr);
                      if (Array.isArray(parsed) && parsed.length > 0) {
                        setCurriculum(parsed);
                        fetch(`${cleanUrl}/scout_groups/${room}/curriculum.json`, {
                          method: "PUT",
                          headers: { "Content-Type": "application/json" },
                          body: JSON.stringify(parsed)
                        }).catch(() => {});
                      }
                    }
                  } catch(e) {}
                }

                if (Array.isArray(remote.notifications)) setNotifications(remote.notifications);

                // Badge awards merge
                if (Array.isArray(remote.badgeAwards)) {
                  let mergedBadges = remote.badgeAwards;
                  try {
                    const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                    const saved = localStorage.getItem(`scout_badge_awards_${activeTroop}`) || localStorage.getItem(`scout_badge_awards_${groupCode}`);
                    if (saved) {
                      const parsed = JSON.parse(saved);
                      if (Array.isArray(parsed) && parsed.length > 0) {
                        const map = new Map();
                        remote.badgeAwards.forEach(b => { if (b && b.id) map.set(b.id, b); });
                        parsed.forEach(b => { if (b && b.id && !map.has(b.id)) map.set(b.id, b); });
                        mergedBadges = Array.from(map.values());
                      }
                    }
                  } catch(e) {}
                  setBadgeAwards(mergedBadges);
                  const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                  localStorage.setItem(`scout_badge_awards_${activeTroop}`, JSON.stringify(mergedBadges));
                  localStorage.setItem(`scout_badge_awards_${groupCode}`, JSON.stringify(mergedBadges));
                }

                if (Array.isArray(remote.supervisorAccounts)) setSupervisorAccounts(remote.supervisorAccounts);

                if (Array.isArray(remote.troopUnits) && remote.troopUnits.length > 0) {
                  setTroopUnits(remote.troopUnits);
                  try {
                    const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                    localStorage.setItem(`scout_troop_units_${groupCode}`, JSON.stringify(remote.troopUnits));
                    localStorage.setItem(`scout_troop_units_${activeTroop}`, JSON.stringify(remote.troopUnits));
                  } catch(e) {}
                }

                // Scout attendance merge (deep merge by date key to preserve every session)
                try {
                  const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                  const savedAtt = localStorage.getItem(`scout_att_history_${activeTroop}`) || localStorage.getItem(`scout_att_history_${groupCode}`);
                  const localParsed = savedAtt ? JSON.parse(savedAtt) : {};
                  const remoteAtt = (remote.scoutAttendanceHistory && typeof remote.scoutAttendanceHistory === "object") ? remote.scoutAttendanceHistory : {};
                  const mergedAtt = { ...localParsed };
                  Object.keys(remoteAtt).forEach(d => {
                    mergedAtt[d] = { ...(mergedAtt[d] || {}), ...remoteAtt[d] };
                  });
                  if (Object.keys(mergedAtt).length > 0) {
                    setScoutAttendanceHistory(mergedAtt);
                    localStorage.setItem(`scout_att_history_${activeTroop}`, JSON.stringify(mergedAtt));
                    localStorage.setItem(`scout_att_history_${groupCode}`, JSON.stringify(mergedAtt));
                    if (Object.keys(mergedAtt).length > Object.keys(remoteAtt).length) {
                      fetch(`${cleanUrl}/scout_groups/${room}/scoutAttendanceHistory.json`, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(mergedAtt)
                      }).catch(() => {});
                    }
                  }
                } catch(e) {}

                // Leader attendance merge (deep merge by date key to preserve every session)
                try {
                  const activeTroop = (currentUser && currentUser.groupCode) ? currentUser.groupCode : (groupCode || "الفوج-الكشفي-01");
                  const savedLdrAtt = localStorage.getItem(`scout_leader_att_history_${activeTroop}`) || localStorage.getItem(`scout_leader_att_history_${groupCode}`);
                  const localParsedLdr = savedLdrAtt ? JSON.parse(savedLdrAtt) : {};
                  const remoteLdrAtt = (remote.leaderAttendanceHistory && typeof remote.leaderAttendanceHistory === "object") ? remote.leaderAttendanceHistory : {};
                  const mergedLdrAtt = { ...localParsedLdr };
                  Object.keys(remoteLdrAtt).forEach(k => {
                    mergedLdrAtt[k] = { ...(mergedLdrAtt[k] || {}), ...remoteLdrAtt[k] };
                  });
                  if (Object.keys(mergedLdrAtt).length > 0) {
                    setLeaderAttendanceHistory(mergedLdrAtt);
                    localStorage.setItem(`scout_leader_att_history_${activeTroop}`, JSON.stringify(mergedLdrAtt));
                    localStorage.setItem(`scout_leader_att_history_${groupCode}`, JSON.stringify(mergedLdrAtt));
                    if (Object.keys(mergedLdrAtt).length > Object.keys(remoteLdrAtt).length) {
                      fetch(`${cleanUrl}/scout_groups/${room}/leaderAttendanceHistory.json`, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(mergedLdrAtt)
                      }).catch(() => {});
                    }
                  }
                } catch(e) {}"""

text = text.replace(old_pull_body_exact, new_pull_body, 1)

# 4. Update markAllScoutsPresent
m_scouts_s1 = text.find("const markAllScoutsPresent = () => {")
m_scouts_s2 = text.find("addNotification(", m_scouts_s1)
assert m_scouts_s1 != -1 and m_scouts_s2 != -1, "Error: markAllScoutsPresent not found"
old_mark_scouts_exact = text[m_scouts_s1:m_scouts_s2]

new_mark_scouts_exact = """const markAllScoutsPresent = () => {
        const dateKey = scoutAttendanceDate;
        const currentRecord = scoutAttendanceHistory[dateKey] || {};
        const updatedDayRecord = { ...currentRecord };

        const updatedScoutsList = scouts.map(sc => {
          if (!visibleScouts.some(vs => vs.id === sc.id)) return sc;
          const prevStatus = currentRecord[sc.id];
          updatedDayRecord[sc.id] = "present";
          if (prevStatus === "absent") {
            return { ...sc, absences: Math.max(0, (sc.absences || 0) - 1) };
          }
          return sc;
        });
        saveScouts(updatedScoutsList);

        const updatedHistory = { ...scoutAttendanceHistory, [dateKey]: updatedDayRecord };
        saveScoutAttendance(updatedHistory);

        """

text = text.replace(old_mark_scouts_exact, new_mark_scouts_exact, 1)

# 5. Update setIndividualScoutAttendance
ind_scouts_s1 = text.find("const setIndividualScoutAttendance = (scout, newStatus) => {")
ind_scouts_s2 = text.find("if (newStatus === \"absent\") {", ind_scouts_s1)
assert ind_scouts_s1 != -1 and ind_scouts_s2 != -1, "Error: setIndividualScoutAttendance not found"
old_ind_scouts_exact = text[ind_scouts_s1:ind_scouts_s2]

new_ind_scouts_exact = """const setIndividualScoutAttendance = (scout, newStatus) => {
        const dateKey = scoutAttendanceDate;
        const currentRecord = scoutAttendanceHistory[dateKey] || {};
        const currentStatus = currentRecord[scout.id];

        if (currentStatus === newStatus) {
          showToast(newStatus === "present" ? "تم تسجيل حضور الفتى مسبقاً لهذا اليوم" : "تم تسجيل غياب الفتى مسبقاً لهذا اليوم");
          return;
        }

        const updatedScoutsList = scouts.map(s => {
          if (s.id !== scout.id) return s;
          let newAbsences = s.absences || 0;
          if (newStatus === "absent" && currentStatus !== "absent") {
            newAbsences = newAbsences + 1;
          } else if (newStatus === "present" && currentStatus === "absent") {
            newAbsences = Math.max(0, newAbsences - 1);
          }
          return {
            ...s,
            absences: newAbsences,
            lastAbsenceDate: newStatus === "absent" ? dateKey : s.lastAbsenceDate
          };
        });
        saveScouts(updatedScoutsList);

        const updatedHistory = {
          ...scoutAttendanceHistory,
          [dateKey]: {
            ...(scoutAttendanceHistory[dateKey] || {}),
            [scout.id]: newStatus
          }
        };
        saveScoutAttendance(updatedHistory);

        """

text = text.replace(old_ind_scouts_exact, new_ind_scouts_exact, 1)

# 6. Update markAllLeadersPresent
m_ldrs_s1 = text.find("const markAllLeadersPresent = () => {")
m_ldrs_s2 = text.find("const sessionLabel =", m_ldrs_s1)
assert m_ldrs_s1 != -1 and m_ldrs_s2 != -1, "Error: markAllLeadersPresent not found"
old_mark_ldrs_exact = text[m_ldrs_s1:m_ldrs_s2]

new_mark_ldrs_exact = """const markAllLeadersPresent = () => {
        const dateKey = `${leaderAttendanceDate}_${leaderSessionType}`;
        const currentRecord = leaderAttendanceHistory[dateKey] || {};
        const updatedDayRecord = { ...currentRecord };

        const updatedLeaders = leadersTracking.map(ldr => {
          const prevStatus = currentRecord[ldr.id];
          updatedDayRecord[ldr.id] = "present";
          if (prevStatus === "present") return ldr;
          if (leaderSessionType === "weekly") {
            return { ...ldr, weeklyPresence: (ldr.weeklyPresence || 0) + 1 };
          } else if (leaderSessionType === "meeting") {
            return { ...ldr, meetingPresence: (ldr.meetingPresence || 0) + 1 };
          } else {
            return { ...ldr, campPresence: (ldr.campPresence || 0) + 1 };
          }
        });
        setLeadersTracking(updatedLeaders);

        const updatedLdrHistory = { ...leaderAttendanceHistory, [dateKey]: updatedDayRecord };
        saveLeaderAttendance(updatedLdrHistory);
        pushToCloud({ leadersTracking: updatedLeaders, leaderAttendanceHistory: updatedLdrHistory });

        """

text = text.replace(old_mark_ldrs_exact, new_mark_ldrs_exact, 1)

# 7. Update setIndividualLeaderAttendance
ind_ldrs_s1 = text.find("const setIndividualLeaderAttendance = (ldr, newStatus) => {")
ind_ldrs_s2 = text.find("const sessionLabel = leaderSessionType === \"weekly\"", ind_ldrs_s1)
assert ind_ldrs_s1 != -1 and ind_ldrs_s2 != -1, "Error: setIndividualLeaderAttendance not found"
old_ind_ldrs_exact = text[ind_ldrs_s1:ind_ldrs_s2]

new_ind_ldrs_exact = """const setIndividualLeaderAttendance = (ldr, newStatus) => {
        const dateKey = `${leaderAttendanceDate}_${leaderSessionType}`;
        const currentRecord = leaderAttendanceHistory[dateKey] || {};
        const currentStatus = currentRecord[ldr.id];

        if (currentStatus === newStatus) {
          showToast(newStatus === "present" ? "تم تسجيل حضور القائد مسبقاً لهذه الحصة والتاريخ" : "تم تسجيل غياب القائد مسبقاً لهذه الحصة والتاريخ");
          return;
        }

        const updatedLeaders = leadersTracking.map(l => {
          if (l.id !== ldr.id) return l;
          if (newStatus === "present" && currentStatus !== "present") {
            if (leaderSessionType === "weekly") return { ...l, weeklyPresence: (l.weeklyPresence || 0) + 1 };
            if (leaderSessionType === "meeting") return { ...l, meetingPresence: (l.meetingPresence || 0) + 1 };
            return { ...l, campPresence: (l.campPresence || 0) + 1 };
          } else if (newStatus === "absent" && currentStatus === "present") {
            if (leaderSessionType === "weekly") return { ...l, weeklyPresence: Math.max(0, (l.weeklyPresence || 0) - 1) };
            if (leaderSessionType === "meeting") return { ...l, meetingPresence: Math.max(0, (l.meetingPresence || 0) - 1) };
            return { ...l, campPresence: Math.max(0, (l.campPresence || 0) - 1) };
          }
          return l;
        });
        setLeadersTracking(updatedLeaders);

        const updatedLdrHistory = {
          ...leaderAttendanceHistory,
          [dateKey]: {
            ...(leaderAttendanceHistory[dateKey] || {}),
            [ldr.id]: newStatus
          }
        };
        saveLeaderAttendance(updatedLdrHistory);
        pushToCloud({ leadersTracking: updatedLeaders, leaderAttendanceHistory: updatedLdrHistory });

        """

text = text.replace(old_ind_ldrs_exact, new_ind_ldrs_exact, 1)

# 8. Update auto-sync dependencies
old_sync_deps = """[scouts, annualPlan, leadersTracking, curriculum, notifications, badgeAwards, troopUnits]"""
new_sync_deps = """[scouts, annualPlan, leadersTracking, curriculum, notifications, badgeAwards, troopUnits, scoutAttendanceHistory, leaderAttendanceHistory]"""
assert old_sync_deps in text, "Error: old_sync_deps not found"
text = text.replace(old_sync_deps, new_sync_deps, 1)

# 9. Update Word curriculum upload
old_upload_word = """if (wordParsedPreview.length === 0) return;
                      setCurriculum(wordParsedPreview);
                      addNotification(
                        "رفع منهاج كشفي جديد",
                        `قام ${currentUser.name} برفع وتحديث المنهاج الكشفي من ملف Word (${wordParsedPreview.reduce((a,c) => a + c.items.length, 0)} متطلب)`,
                        "curriculum"
                      );
                      pushToCloud(undefined, undefined, undefined, wordParsedPreview);
                      setShowUploadCurriculumModal(false);
                      showToast("تم اعتماد المنهاج الكشفي الجديد ومزامنته في لوح المشرف بنجاح");"""

new_upload_word = """if (wordParsedPreview.length === 0) return;
                      saveCurriculum(wordParsedPreview);
                      addNotification(
                        "رفع منهاج كشفي جديد",
                        `قام ${currentUser.name} برفع وتحديث المنهاج الكشفي من ملف Word (${wordParsedPreview.reduce((a,c) => a + c.items.length, 0)} متطلب)`,
                        "curriculum"
                      );
                      setShowUploadCurriculumModal(false);
                      showToast("تم اعتماد وحفظ المنهاج الكشفي الجديد ومزامنته سحابياً بنجاح");"""

assert old_upload_word in text, "Error: old_upload_word not found"
text = text.replace(old_upload_word, new_upload_word, 1)

# 10. Update saveCurriculumFromTable
old_table_save = """const newCurriculum = Object.values(catMap);
        setCurriculum(newCurriculum);
        try {
          localStorage.setItem(`scout_curriculum_${groupCode}`, JSON.stringify(newCurriculum));
        } catch (_) {}
        pushToCloud(undefined, undefined, undefined, newCurriculum);"""

new_table_save = """const newCurriculum = Object.values(catMap);
        saveCurriculum(newCurriculum);"""

assert old_table_save in text, "Error: old_table_save not found"
text = text.replace(old_table_save, new_table_save, 1)

# 11. Update showAddPlanModal
old_add_plan = """const newPlan = {
                      id: "plan-" + Date.now(),
                      title: form.title.value.trim(),
                      date: form.date.value,
                      type: form.type.value,
                      leader: currentUser.name,
                      notes: form.notes.value.trim()
                    };
                    setAnnualPlan(prev => [...prev, newPlan]);
                    addNotification("إضافة نشاط للخطة السنوية", `قام القائد ${currentUser.name} ببرمجة نشاط: ${newPlan.title} (${newPlan.date} - ${newPlan.type})`, "plan");
                    setShowAddPlanModal(false);
                    showToast("تمت إضافة النشاط للخطة السنوية بنجاح");"""

new_add_plan = """const newPlan = {
                      id: "plan-" + Date.now(),
                      title: form.title.value.trim(),
                      date: form.date.value,
                      type: form.type.value,
                      leader: currentUser.name,
                      notes: form.notes.value.trim()
                    };
                    const updated = [...annualPlan, newPlan];
                    saveAnnualPlan(updated);
                    addNotification("إضافة نشاط للخطة السنوية", `قام القائد ${currentUser.name} ببرمجة نشاط: ${newPlan.title} (${newPlan.date} - ${newPlan.type})`, "plan");
                    setShowAddPlanModal(false);
                    showToast("تمت إضافة النشاط للخطة السنوية بنجاح ومزامنته سحابياً");"""

assert old_add_plan in text, "Error: old_add_plan not found"
text = text.replace(old_add_plan, new_add_plan, 1)

# 12. Update showAddBadgeModal
old_add_badge = """setBadgeAwards(prev => {
                      const updated = [newBadge, ...prev];
                      localStorage.setItem(`scout_badge_awards_${groupCode}`, JSON.stringify(updated));
                      pushToCloud(undefined, undefined, undefined, undefined, updated);
                      return updated;
                    });"""

new_add_badge = """const updatedBadges = [newBadge, ...badgeAwards];
                    saveBadgeAwards(updatedBadges);"""

assert old_add_badge in text, "Error: old_add_badge not found"
text = text.replace(old_add_badge, new_add_badge, 1)

# 13. Update annual plan activity documentation
old_doc_plan = """setAnnualPlan(updatedPlan);
                    localStorage.setItem(`scout_plan_${groupCode}`, JSON.stringify(updatedPlan));
                    pushToCloud(undefined, updatedPlan);"""

new_doc_plan = """saveAnnualPlan(updatedPlan);"""

assert old_doc_plan in text, "Error: old_doc_plan not found"
text = text.replace(old_doc_plan, new_doc_plan, 1)

# 14. Update annual plan unmark
old_unmark_plan = """setAnnualPlan(prev => {
                                      const updated = prev.map(p => p.id === item.id ? { ...p, isCompleted: false, completionNotes: "" } : p);
                                      localStorage.setItem(`scout_plan_${groupCode}`, JSON.stringify(updated));
                                      pushToCloud(undefined, updated);
                                      return updated;
                                    });"""

new_unmark_plan = """const updated = annualPlan.map(p => p.id === item.id ? { ...p, isCompleted: false, completionNotes: "" } : p);
                                    saveAnnualPlan(updated);"""

assert old_unmark_plan in text, "Error: old_unmark_plan not found"
text = text.replace(old_unmark_plan, new_unmark_plan, 1)

# 15. Update badge deletion in unit view and supervisor view
old_del_badge1 = """setBadgeAwards(prev => {
                                              const updated = prev.filter(b => b.id !== item.id);
                                              localStorage.setItem(`scout_badge_awards_${groupCode}`, JSON.stringify(updated));
                                              pushToCloud(undefined, undefined, undefined, undefined, updated);
                                              return updated;
                                            });"""

new_del_badge1 = """const updated = badgeAwards.filter(b => b.id !== item.id);
                                            saveBadgeAwards(updated);"""

assert old_del_badge1 in text, "Error: old_del_badge1 not found"
text = text.replace(old_del_badge1, new_del_badge1, 1)

old_del_badge2 = """setBadgeAwards(prev => {
                                                const updated = prev.filter(b => b.id !== item.id);
                                                localStorage.setItem(`scout_badge_awards_${groupCode}`, JSON.stringify(updated));
                                                pushToCloud(undefined, undefined, undefined, undefined, updated);
                                                return updated;
                                              });"""

new_del_badge2 = """const updated = badgeAwards.filter(b => b.id !== item.id);
                                                saveBadgeAwards(updated);"""

assert old_del_badge2 in text, "Error: old_del_badge2 not found"
text = text.replace(old_del_badge2, new_del_badge2, 1)

with open(source_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully applied ALL patches to app.source.jsx!")
