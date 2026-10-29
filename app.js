/* 璇枃涔︽ 路 涓婚〉 / 璺緞 / 璁板綍 */
(function () {
  const DATA = window.CHINESE_DESK_DATA;
  const P = window.ChineseProgress;
  if (!DATA || !P) return;

  const $ = (id) => document.getElementById(id);
  const state = {
    view: "home",
    node: null,
    module: null,
    cards: [],
    idx: 0,
    wrong: [],
    printIndex: null,
  };

  function loadPrintIndex() {
    return fetch("./print-index.json?v=39")
      .then((r) => r.json())
      .then((j) => {
        state.printIndex = j;
      })
      .catch(() => {
        state.printIndex = null;
      });
  }

  function lessonPrint(node) {
    if (!state.printIndex || !node || node.type !== "lesson") return null;
    return state.printIndex.lessons[String(node.bookNo)] || null;
  }

  function openPdf(url) {
    if (!url) return;
    url = String(url).replace(/\\/g, "/");
    var sep = url.indexOf("?") >= 0 ? "&" : "?";
    window.open(encodeURI(url) + sep + "v=21", "_blank");
  }

  function showView(name) {
    state.view = name;
    ["Home", "Path", "Records", "Lesson"].forEach((k) => {
      const el = $("screen" + k);
      if (el) el.classList.toggle("hidden", name.toLowerCase() !== k.toLowerCase());
    });
    const showNav = name === "home" || name === "path" || name === "records";
    $("appNav").classList.toggle("hidden", !showNav);
    document.querySelectorAll(".nav-item").forEach((btn) => {
      btn.classList.toggle("is-on", btn.dataset.nav === name);
    });
    if (name === "home") renderHome();
    if (name === "path") renderPath();
    if (name === "records") renderRecords();
  }

  function modulesFor(node) {
    if (!node) return [];
    if (node.type === "garden") {
      return [
        { id: "garden_write", label: "鏃ョН鏈堢疮杩囧叧", blurb: "绾?0鈥?5鍒嗛挓 路 琛ュ叏/濉┖" },
        { id: "garden_meaning", label: "鎹剰鍐欏彞", blurb: "缁欏嚭鎰忔€濓紝鍐欏嚭鍘熷彞" },
        { id: "garden_bg", label: "浣滆€呬笌鑳屾櫙", blurb: "浜嗚В鏄皝銆佷负浠€涔堥噸瑕? },
      ];
    }
    const les = node.lesson;
    const mods = [];
    if (les.words && les.words.length) mods.push({ id: "words", label: "瀛楄瘝榛樺啓", blurb: "鐪嬫嫾闊冲啓璇嶈" });
    if (les.compounds && les.compounds.length) mods.push({ id: "compounds", label: "褰㈣繎缁勮瘝", blurb: "鍖哄垎褰㈣繎瀛? });
    if (les.polyphones && les.polyphones.length) mods.push({ id: "poly", label: "澶氶煶瀛?, blurb: "閫夋纭闊? });
    if (les.recite) mods.push({ id: "recite", label: "璇炬枃榛樺啓", blurb: les.recite.label || "鑳岃鐗囨" });
    if (les.meaning) mods.push({ id: "meaning", label: "璇炬枃澶ф剰", blurb: "鐞嗚В涓庤〃杈? });
    return mods;
  }

  function renderHome() {
    const store = P.ensure();
    const node = P.currentNode();
    state.node = node;
    $("streakLine").innerHTML = "杩炵画 <strong>" + (store.streak.count || 0) + "</strong> 澶?;
    $("sessionEyebrow").textContent = node.unitTitle || DATA.book;
    $("sessionTitle").textContent =
      node.type === "garden" ? node.title : "绗? + node.bookNo + "璇?路 " + node.title;
    const printBtn = $("btnPrintToday");
    if (printBtn) printBtn.textContent = "缁冧範涓嬭浇";
    $("sessionMeta").textContent =
      (node.kind || "璇炬枃") + " 路 鎵撳嵃鍚庤嚜宸卞仛 路 鍋氬畬鍐嶇湅绛旀";
    const unitEl = $("unitLine");
    if (unitEl) unitEl.textContent = (DATA.book || "") + (node.unitTitle ? " 路 " + node.unitTitle : "");
    const sumEl = $("pathSummary");
    if (sumEl) {
      const path = P.semesterPath();
      sumEl.textContent =
        "鏈鏈?" + P.completedCount() + " / " + path.length + " 绔欏凡缁?;
    }
  }

  function renderPath() {
    const store = P.ensure();
    const path = P.semesterPath();
    $("pathMeta").textContent = "鍏?" + path.length + " 绔?路 宸茬粌 " + P.completedCount() + " 绔欙紙鍚洯鍦?/ 鍔犵粌 / 鍐插埡 / 鎽稿簳锛?;
    const host = $("pathList");
    host.innerHTML = "";
    let lastUnit = "";
    path.forEach((node) => {
      if (node.unitTitle !== lastUnit) {
        lastUnit = node.unitTitle;
        const h = document.createElement("div");
        h.className = "path-unit";
        h.textContent = node.unitTitle;
        host.appendChild(h);
      }
      const done = store.completed[node.id] && store.completed[node.id].count > 0;
      const current = node.type === "lesson" && node.bookNo === store.currentBookLesson;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "path-node" + (done ? " is-done" : "") + (current ? " is-current" : "");
      const badge =
        node.type === "garden"
          ? "鍥?
          : node.type === "weak"
            ? "缁?
            : node.type === "sprint"
            ? "鍐?
            : node.type === "full"
              ? "鎽?
              : String(node.bookNo);
      btn.innerHTML =
        '<span class="path-badge">' +
        badge +
        '</span><span class="path-copy"><strong>' +
        node.title +
        "</strong><small>" +
        (node.kind || "") +
        (done ? " 路 宸茬粌" + store.completed[node.id].count + "椤? : "") +
        (current ? " 路 浠婃棩" : "") +
        "</small></span>";
      btn.addEventListener("click", () => openNodePicker(node));
      host.appendChild(btn);
    });
  }

  function openNodePicker(node) {
    state.node = node;
    $("pathLessonTitle").textContent =
      node.type === "lesson" ? "绗? + node.bookNo + "璇?路 " + node.title : node.title;
    $("pathLessonMeta").textContent = node.unitTitle + " 路 " + (node.kind || "");
    const grid = $("pathModGrid");
    grid.innerHTML = "";
    const pi = state.printIndex || {};

    if (node.type === "lesson") {
      const pr = lessonPrint(node);
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "mod-btn is-primary";
      dl.innerHTML = "缁冧範涓嬭浇<small>绾?0鈥?5鍒嗛挓 路 鍙墦鍗?A4</small>";
      dl.addEventListener("click", () => {
        if (pr && pr.daily) openPdf(pr.daily);
        if (pr && pr.recite) setTimeout(() => openPdf(pr.recite), 400);
      });
      grid.appendChild(dl);

      const ans = document.createElement("button");
      ans.type = "button";
      ans.className = "mod-btn is-answer";
      ans.innerHTML = "绛旀鍦ㄧ嚎鐪?small>鍋氬畬鍐嶇湅 路 涔熷彲涓嬭浇</small>";
      ans.addEventListener("click", () => openAnswers(node));
      grid.appendChild(ans);

      const setCur = document.createElement("button");
      setCur.type = "button";
      setCur.className = "mod-btn";
      setCur.innerHTML = "璁句负浠婃棩璇炬枃<small>涓婚〉灏嗘樉绀鸿繖涓€璇?/small>";
      setCur.addEventListener("click", () => {
        P.setCurrentBookLesson(node.bookNo);
        $("pathLessonOverlay").classList.add("hidden");
        showView("home");
      });
      grid.appendChild(setCur);
    } else if (node.type === "garden") {
      const gPrint = pi.gardens && pi.gardens[node.unitId];
      const daily = gPrint && gPrint.daily;
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "mod-btn is-primary";
      dl.innerHTML = "缁冧範涓嬭浇<small>绾?0鈥?5鍒嗛挓 路 鏃ョН鏈堢疮杩囧叧 路 A4</small>";
      dl.addEventListener("click", () => {
        if (daily) openPdf(daily);
        else alert("鏈洯鍦扮粌涔犳鍦ㄥ噯澶囷紝璇风◢鍚庡啀璇曘€?);
      });
      grid.appendChild(dl);
      const ans = document.createElement("button");
      ans.type = "button";
      ans.className = "mod-btn is-answer";
      ans.innerHTML = "绛旀鍦ㄧ嚎鐪?small>涓庢墦鍗扮増鍚屼竴浠?A4</small>";
      ans.addEventListener("click", () => openGardenAnswers(node));
      grid.appendChild(ans);
      const markG = document.createElement("button");
      markG.type = "button";
      markG.className = "mod-btn";
      markG.innerHTML = "鍗烽潰瀵圭収<small>绾㈢瑪鍦堝嚭閿欓鍏ュ簱</small>";
      markG.addEventListener("click", () => {
        $("pathLessonOverlay").classList.add("hidden");
        if (window.ChineseMarkSheet) {
          ChineseMarkSheet.open({
            unitId: node.unitId,
            source: "garden",
            node: node,
            getPrintIndex: () => state.printIndex,
          });
        }
      });
      grid.appendChild(markG);
    } else if (node.type === "weak") {
      const sk = (pi.skills && pi.skills.byUnit && pi.skills.byUnit[node.unitId]) || {};
      const daily = sk.daily || (pi.skills && pi.skills.weak);
      const ansPdf = sk.answers || (pi.skills && pi.skills.weakAnswers);
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "mod-btn is-primary";
      dl.innerHTML = "涓嬭浇鍔犵粌<small>璇婚煶 路 褰㈣繎 路 鎴愯 路 鐨勫湴寰?路 鎶撳ぇ鎰?/small>";
      dl.addEventListener("click", () => {
        if (daily) openPdf(daily);
        else alert("鏈崟鍏冨姞缁冩鍦ㄥ噯澶?);
      });
      grid.appendChild(dl);
      const ans = document.createElement("button");
      ans.type = "button";
      ans.className = "mod-btn is-answer";
      ans.innerHTML = "鍔犵粌绛旀<small>鍋氬畬鍐嶇湅</small>";
      ans.addEventListener("click", () => {
        if (ansPdf) openPdf(ansPdf);
        else alert("绛旀椤靛皻鏈笂浼?);
      });
      grid.appendChild(ans);
      const done = document.createElement("button");
      done.type = "button";
      done.className = "mod-btn";
      done.innerHTML = "鏍囪宸茬粌<small>璁板叆璺緞杩涘害</small>";
      done.addEventListener("click", () => {
        P.markDone(node.id, "weak");
        $("pathLessonOverlay").classList.add("hidden");
        renderPath();
      });
      grid.appendChild(done);
    } else if (node.type === "sprint") {
      const sp = pi.sprint && pi.sprint[node.unitId];
      const spAns = pi.sprintAnswers && pi.sprintAnswers[node.unitId];
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "mod-btn is-primary";
      dl.innerHTML = "涓嬭浇鍐插埡鍗?small>鑰冨墠 路 鍙墦鍗?A4</small>";
      dl.addEventListener("click", () => {
        if (sp) openPdf(sp);
        else alert("鏈崟鍏冨啿鍒哄嵎灏氭湭涓婁紶");
      });
      grid.appendChild(dl);
      const ans = document.createElement("button");
      ans.type = "button";
      ans.className = "mod-btn is-answer";
      ans.innerHTML = "鍐插埡绛旀<small>鍗曠嫭绛旀椤?路 鍙墦鍗?/small>";
      ans.addEventListener("click", () => {
        if (spAns) openPdf(spAns);
        else alert("鏈崟鍏冨啿鍒虹瓟妗堝皻鏈笂浼?);
      });
      grid.appendChild(ans);
      const mark = document.createElement("button");
      mark.type = "button";
      mark.className = "mod-btn";
      mark.innerHTML = "鍗烽潰瀵圭収<small>绾㈢瑪鍦堝嚭閿欓鍏ュ簱</small>";
      mark.addEventListener("click", () => {
        $("pathLessonOverlay").classList.add("hidden");
        if (window.ChineseMarkSheet) {
          ChineseMarkSheet.open({
            unitId: node.unitId,
            source: "sprint",
            node: node,
            getPrintIndex: () => state.printIndex,
          });
        }
      });
      grid.appendChild(mark);
      const done = document.createElement("button");
      done.type = "button";
      done.className = "mod-btn";
      done.innerHTML = "鏍囪宸茬粌<small>璁板叆璺緞杩涘害</small>";
      done.addEventListener("click", () => {
        P.markDone(node.id, "sprint");
        $("pathLessonOverlay").classList.add("hidden");
        renderPath();
      });
      grid.appendChild(done);
    } else if (node.type === "full") {
      const full = pi.full && pi.full[node.unitId];
      const fullAns = pi.fullAnswers && pi.fullAnswers[node.unitId];
      const school = pi.school && pi.school[node.unitId];
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "mod-btn is-primary";
      dl.innerHTML = "涓嬭浇鎽稿簳鍗?small>瀹屾暣鍗?路 鍙墦鍗?A4</small>";
      dl.addEventListener("click", () => {
        if (full) openPdf(full);
        else alert("鏈崟鍏冩殏鏃犲畬鏁存懜搴曞嵎");
      });
      grid.appendChild(dl);
      const ans = document.createElement("button");
      ans.type = "button";
      ans.className = "mod-btn is-answer";
      ans.innerHTML = "鎽稿簳绛旀<small>鍗曠嫭绛旀椤?路 鍙墦鍗?/small>";
      ans.addEventListener("click", () => {
        if (fullAns) openPdf(fullAns);
        else alert("鏈崟鍏冩殏鏃犳懜搴曠瓟妗?);
      });
      grid.appendChild(ans);
      const mark = document.createElement("button");
      mark.type = "button";
      mark.className = "mod-btn";
      mark.innerHTML = "鍗烽潰瀵圭収<small>绾㈢瑪鍦堝嚭閿欓鍏ュ簱</small>";
      mark.addEventListener("click", () => {
        $("pathLessonOverlay").classList.add("hidden");
        if (window.ChineseMarkSheet) {
          ChineseMarkSheet.open({
            unitId: node.unitId,
            source: "full",
            node: node,
            getPrintIndex: () => state.printIndex,
          });
        }
      });
      grid.appendChild(mark);
      if (school) {
        const sch = document.createElement("button");
        sch.type = "button";
        sch.className = "mod-btn is-primary";
        sch.innerHTML = "鏍″唴鐪熷疄鍗?small>瀛╁瓙鍋氳繃鐨勫師鍗?/small>";
        sch.addEventListener("click", () => openPdf(school));
        grid.appendChild(sch);
        const schMark = document.createElement("button");
        schMark.type = "button";
        schMark.className = "mod-btn";
        schMark.innerHTML = "瀵圭収鏍″唴鍗?small>绾㈢瑪鍦堟湰棰橀敊棰?/small>";
        schMark.addEventListener("click", () => {
          $("pathLessonOverlay").classList.add("hidden");
          if (window.ChineseMarkSheet) {
            ChineseMarkSheet.open({
              unitId: node.unitId,
              source: "school",
              node: node,
              getPrintIndex: () => state.printIndex,
            });
          }
        });
        grid.appendChild(schMark);
      }
      const done = document.createElement("button");
      done.type = "button";
      done.className = "mod-btn";
      done.innerHTML = "鏍囪宸茬粌<small>璁板叆璺緞杩涘害</small>";
      done.addEventListener("click", () => {
        P.markDone(node.id, "full");
        $("pathLessonOverlay").classList.add("hidden");
        renderPath();
      });
      grid.appendChild(done);
    }
    $("pathLessonOverlay").classList.remove("hidden");
  }

  function openAnswers(node) {
    const pr = lessonPrint(node) || {};
    $("pathLessonOverlay").classList.add("hidden");
    const box = $("answerOverlay");
    const body = $("answerBody");
    const title = $("answerTitle");
    const n = node.bookNo;
    const pad = String(n).padStart(2, "0");
    title.textContent = "绗? + n + "璇俱€? + node.title + "銆嬬瓟妗?;
    body.innerHTML = "<p class='meta'>鍔犺浇涓€?/p>";
    box.classList.remove("hidden");

    const pdfUrl = pr.answerPdf || "printables/answers/L" + pad + "-" + node.title + "-绛旀.pdf";
    const mdUrl = pr.answerMd || "answers/lessons/L" + pad + "-" + node.title + "-绛旀.md";
    const src = encodeURI(pdfUrl) + "?v=39";

    $("btnAnswerDownload").onclick = () => openPdf(pdfUrl);

    // Online view = same A4 PDF as print/download
    body.innerHTML =
      '<iframe class="a4-iframe" title="A4绛旀棰勮" src="' +
      src +
      '"></iframe>';

    // Fallback text if PDF embed blocked
    const iframe = body.querySelector("iframe");
    if (iframe) {
      iframe.addEventListener("error", () => showAnswerFallback(body, pr, mdUrl));
    }
    // Some browsers don't fire iframe error; offer text toggle quietly via timeout check is noisy 鈥?keep HTML fallback button
    const tip = document.createElement("button");
    tip.type = "button";
    tip.className = "btn-path";
    tip.textContent = "PDF 鎵撲笉寮€锛熺湅鏂囧瓧鐗?;
    tip.addEventListener("click", () => showAnswerFallback(body, pr, mdUrl));
    body.appendChild(tip);
  }

  function showAnswerFallback(body, pr, mdUrl) {
    if (pr && pr.answerHtml) {
      body.innerHTML = '<div class="a4-paper">' + pr.answerHtml + "</div>";
      return;
    }
    fetch(encodeURI(mdUrl) + "?v=39")
      .then((r) => {
        if (!r.ok) throw new Error("missing");
        return r.text();
      })
      .then((text) => {
        body.innerHTML = '<div class="a4-paper">' + renderMd(text) + "</div>";
      })
      .catch(() => {
        body.innerHTML = "<p>绛旀鍔犺浇澶辫触锛岃鐐逛笅鏂逛笅杞?A4 PDF銆?/p>";
      });
  }


  function openGardenAnswers(node) {
    const gPrint =
      (state.printIndex && state.printIndex.gardens && state.printIndex.gardens[node.unitId]) || {};
    $("pathLessonOverlay").classList.add("hidden");
    const body = $("answerBody");
    $("answerTitle").textContent = (node.title || "璇枃鍥湴") + " 路 绛旀";
    body.innerHTML = "<p class='meta'>鍔犺浇涓€?/p>";
    $("answerOverlay").classList.remove("hidden");

    const pdfUrl =
      gPrint.answerPdf ||
      "printables/garden-answers/" + String(node.unitId || "").toUpperCase() + "-garden-answers.pdf";
    const mdUrl = gPrint.answerMd || "answers/gardens/" + (node.unitId || "") + ".md";
    const dlBtn = $("btnAnswerDownload");
    if (dlBtn) {
      dlBtn.textContent = "涓嬭浇 / 鎵撳嵃绛旀锛圓4锛?;
      dlBtn.onclick = () => openPdf(pdfUrl);
    }

    if (true) {  /* prefer A4 PDF; text fallback below */
      body.innerHTML =
        '<iframe class="a4-iframe" title="鍥湴A4绛旀" src="' +
        encodeURI(pdfUrl) +
        '?v=39"></iframe>';
      const tip = document.createElement("button");
      tip.type = "button";
      tip.className = "btn-path";
      tip.textContent = "PDF 鎵撲笉寮€锛熺湅鏂囧瓧鐗?;
      tip.addEventListener("click", () => {
        if (gPrint.answerHtml) showAnswerFallback(body, gPrint, mdUrl);
        else openGardenTips(node);
      });
      body.appendChild(tip);
      return;
    }
    openGardenTips(node);
  }

  function openGardenTips(node) {
    $("pathLessonOverlay").classList.add("hidden");
    const g = node.garden && node.garden.accumulate;
    $("answerTitle").textContent = (node.title || "璇枃鍥湴") + " 路 鏃ョН鏈堢疮";
    let html = "";
    if (g) {
      html += "<p><b>" + (g.title || "鏃ョН鏈堢疮") + "</b></p>";
      if (g.author) html += "<p class='meta'>" + g.author + "</p>";
      if (g.linesDetail && g.linesDetail.length) {
        g.linesDetail.forEach((ln) => {
          html +=
            "<p><b>" +
            (ln.text || "") +
            "</b><br><span class='meta'>" +
            (ln.tip || "") +
            "</span></p>";
        });
      } else if (g.lines) {
        html += "<p style='font-size:1.2rem;font-weight:800;line-height:1.7'>" + g.lines.join("<br>") + "</p>";
      }
      if (g.items) {
        g.items.forEach((it) => {
          html +=
            "<p><b>" +
            (it.text || "") +
            "</b><br><span class='meta'>" +
            (it.who || "") +
            (it.tip ? " 路 " + it.tip : "") +
            "</span></p>";
        });
      }
      if (g.meaning) html += "<p><b>澶ф剰</b><br>" + g.meaning + "</p>";
      if (g.background) html += "<p class='meta'>" + g.background + "</p>";
      if (node.garden && node.garden.extra) html += "<p class='meta'>" + node.garden.extra + "</p>";
    }
    $("answerBody").innerHTML =
      '<div class="a4-paper">' + (html || "<p>鏆傛棤鍐呭</p>") + "</div>";
    const gPrintTips =
      state.printIndex && state.printIndex.gardens && state.printIndex.gardens[node.unitId];
    $("btnAnswerDownload").onclick = () => {
      if (gPrintTips && gPrintTips.answerPdf) openPdf(gPrintTips.answerPdf);
      else if (gPrintTips && gPrintTips.daily) openPdf(gPrintTips.daily);
    };
    $("btnAnswerDownload").textContent = "涓嬭浇 / 鎵撳嵃绛旀锛圓4锛?;
    $("answerOverlay").classList.remove("hidden");
  }

  function renderMd(text) {
    return text
      .split("\n")
      .map((line) => {
        if (line.startsWith("# ")) return "<h2 style='font-family:Noto Serif SC,serif;color:var(--brand-deep);margin:0 0 8px'>" + line.slice(2) + "</h2>";
        if (line.startsWith("## ")) return "<h3 style='color:var(--brand);margin:14px 0 6px'>" + line.slice(3) + "</h3>";
        if (line.startsWith("> ")) return "<p class='meta'>" + line.slice(2) + "</p>";
        if (!line.trim()) return "";
        return "<p style='margin:0 0 8px;line-height:1.55'>" + line + "</p>";
      })
      .join("");
  }

  function buildCards(node, moduleId) {
    const cards = [];
    if (node.type === "garden") {
      const g = node.garden.accumulate;
      if (moduleId === "garden_write") {
        const items =
          g.items ||
          (g.linesDetail
            ? g.linesDetail.map((ln) => ({ text: ln.text, who: g.author }))
            : g.lines
              ? [{ text: g.lines.join(""), who: g.author }]
              : []);
        items.forEach((it) => {
          const full = it.text || "";
          const cut = Math.max(4, Math.floor(full.replace(/[锛屻€傦紵锛併€乚/g, "").length / 2));
          cards.push({
            type: "write",
            title: "鏃ョН鏈堢疮榛樺啓",
            prompt: "琛ュ叏锛? + full.slice(0, cut) + "________",
            answer: full,
            tip: it.who || g.author || "",
            meta: { moduleId, nodeId: node.id, kind: "鍥湴榛樺啓" },
          });
        });
      } else if (moduleId === "garden_meaning") {
        const items =
          g.items ||
          g.linesDetail ||
          [{ text: (g.lines || []).join(""), tip: g.meaning }];
        items.forEach((it) => {
          const tip = (it.tip || g.meaning || "").trim();
          const full = (it.text || "").trim();
          if (!tip || !full) return;
          cards.push({
            type: "write",
            title: "鎹剰鍐欏彞",
            prompt: "鏍规嵁鎰忔€濆啓鍑哄師鍙ワ細\n" + tip,
            answer: full,
            tip: (it.who || g.author || "") ? ("鍑哄锛? + (it.who || g.author)) : "",
            meta: { moduleId, nodeId: node.id, kind: "鎹剰鍐欏彞" },
          });
        });
      } else if (moduleId === "garden_bg") {
        cards.push({
          type: "read",
          title: "浣滆€呬笌鑳屾櫙",
          prompt: g.background || node.garden.accumulate.background || "鏈崟鍏冨洯鍦拌儗鏅?,
          answer: "",
          soft: true,
          meta: { moduleId, nodeId: node.id, kind: "鑳屾櫙" },
        });
      }
      return cards;
    }

    const les = node.lesson;
    if (moduleId === "words") {
      (les.words || []).forEach((w) => {
        cards.push({
          type: "write",
          title: "瀛楄瘝榛樺啓",
          prompt: "鐪嬫嫾闊冲啓璇嶈锛歕n" + w.py,
          answer: w.zh,
          meta: { moduleId, nodeId: node.id, kind: "瀛楄瘝榛樺啓", q: w.py },
        });
      });
    } else if (moduleId === "compounds") {
      (les.compounds || []).forEach((c) => {
        cards.push({
          type: "write",
          title: "褰㈣繎缁勮瘝",
          prompt: "鍒嗗埆缁勮瘝锛? + c.a + "锛堛€€銆€锛夈€€" + c.b + "锛堛€€銆€锛?,
          answer: c.hint,
          tip: "鍙傝€冿細" + c.hint,
          soft: true,
          meta: { moduleId, nodeId: node.id, kind: "缁勮瘝", q: c.a + "/" + c.b },
        });
      });
    } else if (moduleId === "poly") {
      (les.polyphones || []).forEach((p) => {
        cards.push({
          type: "choice",
          title: "澶氶煶瀛?,
          prompt: "缁欍€? + p.word + "銆嶉€夋纭闊?,
          opts: p.opts,
          answer: p.ok,
          meta: { moduleId, nodeId: node.id, kind: "澶氶煶瀛?, q: p.word },
        });
      });
    } else if (moduleId === "recite" && les.recite) {
      cards.push({
        type: "write",
        title: "璇炬枃榛樺啓",
        prompt: (les.recite.label || "璇炬枃榛樺啓") + "\n" + les.recite.prompt,
        answer: les.recite.answer,
        tip: "绛旀锛? + les.recite.answer,
        meta: { moduleId, nodeId: node.id, kind: "璇炬枃榛樺啓" },
      });
    } else if (moduleId === "meaning" && les.meaning) {
      cards.push({
        type: "write",
        title: "璇炬枃澶ф剰",
        prompt: les.meaning.prompt,
        answer: les.meaning.sample,
        tip: "鍙傝€冿細" + les.meaning.sample,
        soft: true,
        meta: { moduleId, nodeId: node.id, kind: "璇炬枃澶ф剰" },
      });
    }
    return cards;
  }

  function startModule(node, moduleId) {
    state.node = node;
    state.module = moduleId;
    state.cards = buildCards(node, moduleId);
    state.idx = 0;
    state.wrong = [];
    if (!state.cards.length) {
      alert("杩欎竴椤硅繕鍦ㄥ噯澶囧唴瀹广€?);
      return;
    }
    showView("lesson");
    renderCard();
  }

  function startTodayFlow() {
    const node = P.currentNode();
    const mods = modulesFor(node);
    if (!mods.length) return;
    openNodePicker(node);
    showView("path");
    // keep overlay from openNodePicker - need to show home then overlay
    showView("home");
    openNodePicker(node);
  }

  function renderCard() {
    const card = state.cards[state.idx];
    const total = state.cards.length;
    $("progressFill").style.width = Math.round((state.idx / total) * 100) + "%";
    $("lessonUnitTitle").textContent = state.node.unitTitle;
    $("lessonNameTitle").textContent =
      state.node.type === "garden"
        ? state.node.title
        : "绗? + state.node.bookNo + "璇?路 " + state.node.title;
    $("cardType").textContent = card.title + " 路 " + (state.idx + 1) + "/" + total;
    $("cardPrompt").textContent = card.prompt;
    $("cardSub").textContent = card.tip && card.type === "read" ? "" : "";
    const extra = $("cardExtra");
    extra.innerHTML = "";
    const actions = $("cardActions");
    actions.innerHTML = "";
    $("cardFeedback").className = "feedback hidden";

    if (card.type === "choice") {
      const row = document.createElement("div");
      row.className = "choice-row";
      card.opts.forEach((opt) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "chip";
        b.textContent = opt;
        b.addEventListener("click", () => gradeChoice(card, opt, b, row));
        row.appendChild(b);
      });
      extra.appendChild(row);
    } else if (card.type === "write") {
      const ta = document.createElement("textarea");
      ta.className = "write-box";
      ta.id = "answerInput";
      ta.placeholder = "鍐欏湪杩欓噷鈥?;
      extra.appendChild(ta);
      const ok = document.createElement("button");
      ok.type = "button";
      ok.className = "btn-start";
      ok.textContent = "瀵圭収绛旀";
      ok.addEventListener("click", () => gradeWrite(card, ta.value));
      actions.appendChild(ok);
    } else if (card.type === "read") {
      const p = document.createElement("p");
      p.className = "card-sub";
      p.style.whiteSpace = "pre-wrap";
      p.textContent = card.prompt;
      $("cardPrompt").textContent = card.title;
      extra.appendChild(p);
      const ok = document.createElement("button");
      ok.type = "button";
      ok.className = "btn-start";
      ok.textContent = "鎴戠煡閬撲簡";
      ok.addEventListener("click", () => nextCard(true));
      actions.appendChild(ok);
    }
  }

  function showFb(text, bad) {
    const el = $("cardFeedback");
    el.className = "feedback" + (bad ? " bad" : "");
    el.textContent = text;
  }

  function gradeChoice(card, opt, btn, row) {
    const good = opt === card.answer;
    row.querySelectorAll(".chip").forEach((c) => c.classList.remove("active", "is-ok", "is-bad"));
    btn.classList.add(good ? "is-ok" : "is-bad");
    if (!good) {
      P.addMistake({
        unit: state.node.unitTitle,
        lesson: state.node.title,
        kind: card.meta.kind,
        q: card.meta.q || card.prompt,
        wrong: opt,
        right: card.answer,
      });
      state.wrong.push(card);
      showFb("涓嶅銆傛纭細銆? + card.answer + "銆戝凡璁″叆閿欓銆?, true);
    } else {
      showFb("姝ｇ‘锛?, false);
    }
    setTimeout(() => nextCard(good), good ? 450 : 900);
  }

  function normalize(s) {
    return String(s || "")
      .replace(/\s+/g, "")
      .replace(/[锛?銆傦紟.銆侊紱;锛?]/g, "");
  }

  function gradeWrite(card, val) {
    if (card.soft) {
      showFb((card.tip || card.answer) + "\n锛堝紑鏀鹃锛氭剰鎬濆鍗冲彲銆傝嫢瀹屽叏涓嶄細鍙偣銆岃閿欓銆嶏級", false);
      const row = document.createElement("div");
      row.className = "lesson-actions";
      const pass = document.createElement("button");
      pass.type = "button";
      pass.className = "btn-start";
      pass.textContent = "杩囧叧锛屼笅涓€棰?;
      pass.addEventListener("click", () => nextCard(true));
      const miss = document.createElement("button");
      miss.type = "button";
      miss.className = "btn-secondary";
      miss.textContent = "涓嶄細锛岃鍏ラ敊棰?;
      miss.addEventListener("click", () => {
        P.addMistake({
          unit: state.node.unitTitle,
          lesson: state.node.title,
          kind: card.meta.kind,
          q: card.prompt.slice(0, 40),
          wrong: val || "锛堢┖锛?,
          right: card.answer,
        });
        state.wrong.push(card);
        nextCard(false);
      });
      $("cardActions").innerHTML = "";
      $("cardActions").appendChild(pass);
      $("cardActions").appendChild(miss);
      return;
    }
    const good = normalize(val).includes(normalize(card.answer)) || normalize(val) === normalize(card.answer);
    // also accept if each part of answer appears
    const parts = String(card.answer).split(/[锛?銆乚/);
    const almost = parts.length > 1 && parts.every((p) => normalize(val).includes(normalize(p)));
    if (good || almost) {
      showFb("寰堝ソ锛佸弬鑰冿細" + card.answer, false);
      setTimeout(() => nextCard(true), 500);
    } else {
      P.addMistake({
        unit: state.node.unitTitle,
        lesson: state.node.title,
        kind: card.meta.kind,
        q: card.meta.q || card.prompt.slice(0, 40),
        wrong: val || "锛堢┖锛?,
        right: card.answer,
      });
      state.wrong.push(card);
      showFb("鍐嶇湅鐪嬨€傛纭弬鑰冿細銆? + card.answer + "銆戝凡璁″叆閿欓銆?, true);
      const next = document.createElement("button");
      next.type = "button";
      next.className = "btn-start";
      next.textContent = "涓嬩竴棰?;
      next.addEventListener("click", () => nextCard(false));
      $("cardActions").innerHTML = "";
      $("cardActions").appendChild(next);
    }
  }

  function nextCard() {
    state.idx += 1;
    if (state.idx >= state.cards.length) {
      finishModule();
      return;
    }
    renderCard();
  }

  function finishModule() {
    P.markDone(state.node.id, state.module);
    $("progressFill").style.width = "100%";
    $("cardType").textContent = "瀹屾垚";
    $("cardPrompt").textContent = "鏈粍缁冧範瀹屾垚";
    $("cardExtra").innerHTML = "";
    $("cardFeedback").className = "feedback";
    $("cardFeedback").textContent =
      state.wrong.length === 0
        ? "鍏ㄥ锛侀敊棰樺鏆傛椂娓呮竻鐖界埥銆?
        : "鏈?" + state.wrong.length + " 澶勫凡杩涢敊棰樿褰曪紝鍙幓銆岃褰曘€嶅涔犮€?;
    const actions = $("cardActions");
    actions.innerHTML = "";
    const home = document.createElement("button");
    home.type = "button";
    home.className = "btn-start";
    home.textContent = "鍥炰富椤?;
    home.addEventListener("click", () => showView("home"));
    const more = document.createElement("button");
    more.type = "button";
    more.className = "btn-secondary";
    more.textContent = "缁х画鏈鍏朵粬缁冧範";
    more.addEventListener("click", () => openNodePicker(state.node));
    actions.appendChild(home);
    actions.appendChild(more);
  }

  const SOURCE_LABEL = {
    daily1: "鏃ュ父鈶?,
    daily2: "鏃ュ父鈶?,
    daily3: "鏃ュ父鈶?,
    sprint: "鍗曞厓鍐插埡",
    full: "鎽稿簳鍗?,
    school: "鏍″唴鐪熷疄鍗?,
    garden: "璇枃鍥湴",
  };

  let mistDraft = { photoBlob: null, photoName: "", qNos: [] };

  function unitLessons(unitId) {
    const u = (DATA.units || []).find((x) => x.id === unitId);
    return (u && u.lessons) || [];
  }

  function sourcePdf(unitId, source) {
    const pi = state.printIndex || {};
    if (source === "sprint") return (pi.sprint && pi.sprint[unitId]) || null;
    if (source === "full") return (pi.full && pi.full[unitId]) || null;
    if (source === "school") return (pi.school && pi.school[unitId]) || null;
    if (source === "garden") {
      const g = pi.gardens && pi.gardens[unitId];
      return (g && g.daily) || null;
    }
    const lessons = unitLessons(unitId);
    const idx = source === "daily2" ? 1 : source === "daily3" ? 2 : 0;
    const les = lessons[idx];
    if (!les) {
      const g = pi.gardens && pi.gardens[unitId];
      return (g && g.daily) || null;
    }
    const pack = pi.lessons && pi.lessons[String(les.bookNo)];
    return (pack && pack.daily) || null;
  }

  function similarPdf(unitId, source) {
    const pi = state.printIndex || {};
    if (source === "sprint" || source === "full" || source === "school") {
      const sk = pi.skills && pi.skills.weak;
      if (sk) return sk;
      const g = pi.gardens && pi.gardens[unitId];
      return (g && g.daily) || sourcePdf(unitId, "daily1");
    }
    const g = pi.gardens && pi.gardens[unitId];
    if (g && g.daily) return g.daily;
    return sourcePdf(unitId, source);
  }

  function fillMistakeForm() {
    const sel = $("mistakeUnit");
    if (!sel) return;
    sel.innerHTML = "";
    (DATA.units || []).forEach((u) => {
      const opt = document.createElement("option");
      opt.value = u.id;
      opt.textContent = u.name.split("路")[0].trim();
      sel.appendChild(opt);
    });
    const host = $("mistakeQnos");
    host.innerHTML = "";
    mistDraft.qNos = [];
    for (let i = 1; i <= 20; i++) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "mist-q";
      b.textContent = String(i);
      b.addEventListener("click", () => {
        const on = b.classList.toggle("is-on");
        if (on) mistDraft.qNos.push(i);
        else mistDraft.qNos = mistDraft.qNos.filter((n) => n !== i);
        mistDraft.qNos.sort((a, c) => a - c);
      });
      host.appendChild(b);
    }
    mistDraft.photoBlob = null;
    mistDraft.photoName = "";
    const prev = $("mistakePreview");
    prev.classList.add("hidden");
    prev.innerHTML = "";
    $("mistakePhoto").value = "";
    $("mistakeNote").value = "";
    $("mistakeSource").value = "daily1";
  }

  function openMistakeEntry() {
    fillMistakeForm();
    $("mistakeOverlay").classList.remove("hidden");
  }

  async function saveMistakeEntry() {
    const DB = window.ChineseMistakesDB;
    if (!DB) {
      alert("閿欓搴撴湭鍔犺浇");
      return;
    }
    if (!mistDraft.qNos.length) {
      alert("璇峰嬀閫夎嚦灏戜竴閬撻敊棰橀鍙凤紙鐓х墖鍙◢鍚庤ˉ锛?);
      return;
    }
    const unitId = $("mistakeUnit").value;
    const source = $("mistakeSource").value;
    const note = ($("mistakeNote").value || "").trim();
    const entry = {
      id: "m" + Date.now(),
      unitId,
      source,
      qNos: mistDraft.qNos.slice(),
      note,
      status: "鏈帉鎻?,
      at: new Date().toISOString().slice(0, 10),
      photoName: mistDraft.photoName || "",
      photoBlob: mistDraft.photoBlob,
    };
    await DB.putEntry(entry);
    $("mistakeOverlay").classList.add("hidden");
    renderRecords();
  }

  async function exportMistakes() {
    const DB = window.ChineseMistakesDB;
    if (!DB) return;
    const data = await DB.exportBackup();
    const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "chinese-desk-mistakes-backup.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }

  async function importMistakes(file) {
    const DB = window.ChineseMistakesDB;
    if (!DB || !file) return;
    const text = await file.text();
    const data = JSON.parse(text);
    const n = await DB.importBackup(data);
    alert("宸插鍏?" + n + " 鏉￠敊棰?);
    renderRecords();
  }

  async function renderRecords() {
    const store = P.ensure();
    const DB = window.ChineseMistakesDB;
    let bank = [];
    try {
      bank = DB ? await DB.listEntries() : [];
    } catch (e) {
      bank = [];
    }
    const openCount = bank.filter((m) => m.status !== "宸叉帉鎻?).length;
    $("recordsScore").innerHTML =
      "杩炵画 <b>" +
      (store.streak.count || 0) +
      "</b> 澶?路 閿欓 <b>" +
      openCount +
      "</b> 鏉?br/><span style='color:var(--muted);font-size:.88rem'>鍘熷嵎涓婄孩绗斿湀棰樺嵆鍙叆搴?/span>";

    const toolbar = $("recordsToolbar");
    if (toolbar) {
      toolbar.innerHTML = "";
      const add = document.createElement("button");
      add.type = "button";
      add.className = "btn-start";
      add.textContent = "褰曞叆閿欓";
      add.addEventListener("click", openMistakeEntry);
      toolbar.appendChild(add);
      const exp = document.createElement("button");
      exp.type = "button";
      exp.className = "btn-path";
      exp.textContent = "瀵煎嚭澶囦唤";
      exp.addEventListener("click", () => exportMistakes());
      toolbar.appendChild(exp);
      const imp = document.createElement("button");
      imp.type = "button";
      imp.className = "btn-warm";
      imp.textContent = "瀵煎叆澶囦唤";
      imp.addEventListener("click", () => {
        const inp = document.createElement("input");
        inp.type = "file";
        inp.accept = "application/json,.json";
        inp.onchange = () => {
          if (inp.files && inp.files[0]) importMistakes(inp.files[0]);
        };
        inp.click();
      });
      toolbar.appendChild(imp);
    }

    const actions = $("recordsActions");
    if (actions) actions.innerHTML = "";

    const list = $("recordsList");
    if ($("recordsMeta")) $("recordsMeta").textContent = "鎴戠殑閿欓锛? + bank.length + "锛?;
    list.innerHTML = "";
    if (!bank.length) {
      list.innerHTML =
        "<p class='path-meta'>杩樻病鏈夐敊棰樸€傜偣涓婃柟銆屽嵎闈㈠鐓с€嶏紝鍦ㄥ師鍗蜂笂鐢ㄧ孩绗斿湀鍑洪敊棰樺嵆鍙叆搴撱€?/p>";
      store.mistakes = [];
      P.save(store);
      return;
    }

    bank.slice(0, 60).forEach((m) => {
      const div = document.createElement("div");
      div.className = "mistake-item";
      const unit = (DATA.units || []).find((u) => u.id === m.unitId);
      const unitName = unit ? unit.name.split("路")[0].trim() : m.unitId;
      const qtxt = (m.qNos || []).join("銆?) || "鈥?;
      const head =
        "<div class='row'><strong>" +
        unitName +
        " 路 " +
        (SOURCE_LABEL[m.source] || m.source) +
        "</strong><small>" +
        (m.at || "") +
        " 路 " +
        (m.status || "") +
        "</small></div>" +
        "<div style='margin:6px 0;font-size:.95rem'>棰樺彿 " +
        qtxt +
        (m.note ? " 路 " + m.note : "") +
        "</div>";
      div.innerHTML = head;

      if (m.photoBlob) {
        const row = document.createElement("div");
        row.style.display = "flex";
        row.style.gap = "10px";
        row.style.alignItems = "flex-start";
        const img = document.createElement("img");
        img.className = "mist-thumb";
        img.alt = "閿欓鍗烽潰";
        img.src = URL.createObjectURL(m.photoBlob);
        img.addEventListener("click", () => window.open(img.src, "_blank"));
        row.appendChild(img);
        const meta = document.createElement("div");
        meta.className = "meta";
        meta.textContent = "鐐圭缉鐣ュ浘鏌ョ湅鍘熷浘瀛樿瘉";
        row.appendChild(meta);
        div.appendChild(row);
      } else {
        const miss = document.createElement("p");
        miss.className = "meta";
        miss.textContent = "鏆傛棤鍗烽潰鐓х墖锛堝彲鐐广€岃ˉ鐓х墖銆嶇◢鍚庢坊鍔狅級";
        div.appendChild(miss);
      }

      const actionsRow = document.createElement("div");
      actionsRow.className = "mist-actions";

      const orig = document.createElement("button");
      orig.type = "button";
      orig.className = "btn-path";
      orig.textContent = "璋冨師棰?;
      orig.addEventListener("click", () => {
        const url = sourcePdf(m.unitId, m.source);
        if (url) openPdf(url);
        else alert("鏈壘鍒板搴旂粌涔?PDF");
      });
      actionsRow.appendChild(orig);

      const sim = document.createElement("button");
      sim.type = "button";
      sim.className = "btn-warm";
      sim.textContent = "鍚岀被缁冧範";
      sim.addEventListener("click", () => {
        const url = similarPdf(m.unitId, m.source);
        if (url) openPdf(url);
        else alert("鏆傛棤鍚岀被缁冧範");
      });
      actionsRow.appendChild(sim);

      const mastered = document.createElement("button");
      mastered.type = "button";
      mastered.className = "btn";
      mastered.textContent = m.status === "宸叉帉鎻? ? "鏍囨湭鎺屾彙" : "鏍囧凡鎺屾彙";
      mastered.addEventListener("click", async () => {
        m.status = m.status === "宸叉帉鎻? ? "鏈帉鎻? : "宸叉帉鎻?;
        await DB.putEntry(m);
        renderRecords();
      });
      actionsRow.appendChild(mastered);

      const photoBtn = document.createElement("button");
      photoBtn.type = "button";
      photoBtn.className = "btn";
      photoBtn.textContent = m.photoBlob ? "鎹㈢収鐗? : "琛ョ収鐗?;
      photoBtn.addEventListener("click", () => {
        const inp = document.createElement("input");
        inp.type = "file";
        inp.accept = "image/*";
        inp.onchange = async () => {
          const f = inp.files && inp.files[0];
          if (!f) return;
          m.photoBlob = f;
          m.photoName = f.name || "photo.jpg";
          await DB.putEntry(m);
          renderRecords();
        };
        inp.click();
      });
      actionsRow.appendChild(photoBtn);

      const del = document.createElement("button");
      del.type = "button";
      del.className = "btn";
      del.textContent = "鍒犻櫎";
      del.addEventListener("click", async () => {
        if (!confirm("鍒犻櫎杩欐潯閿欓锛?)) return;
        await DB.deleteEntry(m.id);
        renderRecords();
      });
      actionsRow.appendChild(del);

      div.appendChild(actionsRow);
      list.appendChild(div);
    });

    store.mistakes = bank.map((m) => ({
      id: m.id,
      unitId: m.unitId,
      source: m.source,
      qNos: m.qNos,
      status: m.status,
      at: m.at,
      note: m.note,
    }));
    P.save(store);
  }

  // events
  $("navHome").addEventListener("click", () => showView("home"));
  $("navPath").addEventListener("click", () => showView("path"));
  $("navRecords").addEventListener("click", () => showView("records"));
  $("btnOpenPath").addEventListener("click", () => showView("path"));
  $("btnPrintToday").addEventListener("click", () => {
    const node = P.currentNode();
    const pr = lessonPrint(node);
    if (pr && pr.daily) {
      openPdf(pr.daily);
      if (pr.recite) setTimeout(() => openPdf(pr.recite), 400);
    } else if (node.type === "lesson") {
      openPdf(
        "printables/lessons/L" +
          String(node.bookNo).padStart(2, "0") +
          "-" +
          node.title +
          "-姣忔棩10鍒嗛挓.pdf"
      );
    } else showView("path");
  });
  const btnAnswers = $("btnViewAnswers");
  if (btnAnswers) {
    btnAnswers.addEventListener("click", () => {
      const node = P.currentNode();
      if (node.type === "garden") openGardenAnswers(node);
      else openAnswers(node);
    });
  }
  const btnCloseAns = $("btnCloseAnswer");
  if (btnCloseAns) {
    btnCloseAns.addEventListener("click", () => $("answerOverlay").classList.add("hidden"));
  }
  $("pathLessonClose").addEventListener("click", () => $("pathLessonOverlay").classList.add("hidden"));
  $("btnCloseLesson").addEventListener("click", () => showView("home"));
  $("btnRecordsToPath").addEventListener("click", () => showView("path"));

  const btnCloseMist = $("btnCloseMistake");
  if (btnCloseMist) {
    btnCloseMist.addEventListener("click", () => $("mistakeOverlay").classList.add("hidden"));
  }
  const photoInp = $("mistakePhoto");
  if (photoInp) {
    photoInp.addEventListener("change", () => {
      const f = photoInp.files && photoInp.files[0];
      if (!f) return;
      mistDraft.photoBlob = f;
      mistDraft.photoName = f.name || "photo.jpg";
      const prev = $("mistakePreview");
      prev.classList.remove("hidden");
      prev.innerHTML = "";
      const img = document.createElement("img");
      img.alt = "棰勮";
      img.src = URL.createObjectURL(f);
      prev.appendChild(img);
    });
  }
  const btnSaveMist = $("btnSaveMistake");
  if (btnSaveMist) {
    btnSaveMist.addEventListener("click", () => {
      saveMistakeEntry().catch((e) => alert("淇濆瓨澶辫触锛? + (e && e.message ? e.message : e)));
    });
  }




  if (window.ChineseMarkSheet) {
    ChineseMarkSheet.bindUi(
      () => state.printIndex,
      () => showView("records")
    );
  }

  // init current lesson 8
  P.ensure();
  loadPrintIndex().finally(() => showView("home"));
})();
