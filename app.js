/* 语文书桌 · 主页 / 路径 / 记录 */
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
    return fetch("./print-index.json?v=4")
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
    window.open(encodeURI(url), "_blank");
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
        { id: "garden_write", label: "日积月累默写", blurb: "名句 / 俗语填空" },
        { id: "garden_meaning", label: "大意理解", blurb: "说说名句意思" },
        { id: "garden_bg", label: "作者与背景", blurb: "了解是谁、为什么重要" },
      ];
    }
    const les = node.lesson;
    const mods = [];
    if (les.words && les.words.length) mods.push({ id: "words", label: "字词默写", blurb: "看拼音写词语" });
    if (les.compounds && les.compounds.length) mods.push({ id: "compounds", label: "形近组词", blurb: "区分形近字" });
    if (les.polyphones && les.polyphones.length) mods.push({ id: "poly", label: "多音字", blurb: "选正确读音" });
    if (les.recite) mods.push({ id: "recite", label: "课文默写", blurb: les.recite.label || "背诵片段" });
    if (les.meaning) mods.push({ id: "meaning", label: "课文大意", blurb: "理解与表达" });
    return mods;
  }

  function renderHome() {
    const store = P.ensure();
    const node = P.currentNode();
    state.node = node;
    $("streakLine").innerHTML = "连续 <strong>" + (store.streak.count || 0) + "</strong> 天";
    $("sessionEyebrow").textContent = node.unitTitle || DATA.book;
    $("sessionTitle").textContent =
      node.type === "garden" ? node.title : "第" + node.bookNo + "课 · " + node.title;
    const printBtn = $("btnPrintToday");
    if (printBtn) printBtn.textContent = "练习下载";
    $("sessionMeta").textContent =
      (node.kind || "课文") + " · 打印后自己做 · 做完再看答案";
    const unitEl = $("unitLine");
    if (unitEl) unitEl.textContent = node.unitTitle || DATA.book;
    const sumEl = $("pathSummary");
    if (sumEl) {
      const path = P.semesterPath();
      sumEl.textContent =
        "本学期 " + P.completedCount() + " / " + path.length + " 站已练";
    }
  }

  function renderPath() {
    const store = P.ensure();
    const path = P.semesterPath();
    $("pathMeta").textContent = "共 " + path.length + " 站 · 已练 " + P.completedCount() + " 站（含园地）";
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
      const badge = node.type === "garden" ? "园" : String(node.bookNo);
      btn.innerHTML =
        '<span class="path-badge">' +
        badge +
        '</span><span class="path-copy"><strong>' +
        node.title +
        "</strong><small>" +
        (node.kind || "") +
        (done ? " · 已练" + store.completed[node.id].count + "项" : "") +
        (current ? " · 今日" : "") +
        "</small></span>";
      btn.addEventListener("click", () => openNodePicker(node));
      host.appendChild(btn);
    });
  }

  function openNodePicker(node) {
    state.node = node;
    $("pathLessonTitle").textContent =
      node.type === "garden" ? node.title : "第" + node.bookNo + "课 · " + node.title;
    $("pathLessonMeta").textContent = node.unitTitle + " · " + (node.kind || "");
    const grid = $("pathModGrid");
    grid.innerHTML = "";

    if (node.type === "lesson") {
      const pr = lessonPrint(node);
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "mod-btn is-primary";
      dl.innerHTML = "练习下载<small>全部题型合订 · 可打印 A4</small>";
      dl.addEventListener("click", () => {
        if (pr && pr.daily) openPdf(pr.daily);
        if (pr && pr.recite) setTimeout(() => openPdf(pr.recite), 400);
      });
      grid.appendChild(dl);

      const ans = document.createElement("button");
      ans.type = "button";
      ans.className = "mod-btn is-answer";
      ans.innerHTML = "答案在线看<small>做完再看 · 也可下载</small>";
      ans.addEventListener("click", () => openAnswers(node));
      grid.appendChild(ans);

      const setCur = document.createElement("button");
      setCur.type = "button";
      setCur.className = "mod-btn";
      setCur.innerHTML = "设为今日课文<small>主页将显示这一课</small>";
      setCur.addEventListener("click", () => {
        P.setCurrentBookLesson(node.bookNo);
        $("pathLessonOverlay").classList.add("hidden");
        showView("home");
      });
      grid.appendChild(setCur);
    } else if (node.type === "garden") {
      const sp = state.printIndex && state.printIndex.sprint && state.printIndex.sprint[node.unitId];
      const dl = document.createElement("button");
      dl.type = "button";
      dl.className = "mod-btn is-primary";
      dl.innerHTML = "练习下载<small>单元冲刺 · 可打印 A4</small>";
      dl.addEventListener("click", () => openPdf(sp));
      grid.appendChild(dl);
      const ans = document.createElement("button");
      ans.type = "button";
      ans.className = "mod-btn is-answer";
      ans.innerHTML = "答案在线看<small>日积月累全文 · 句意 · 可下载</small>";
      ans.addEventListener("click", () => openGardenTips(node));
      grid.appendChild(ans);
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
    title.textContent = "第" + n + "课《" + node.title + "》答案";
    body.innerHTML = "<p class='meta'>加载中…</p>";
    box.classList.remove("hidden");

    const mdUrl = pr.answerMd || "answers/lessons/L" + pad + ".md";
    const pdfUrl = pr.answerPdf || "printables/answers/L" + pad + "-answers.pdf";

    $("btnAnswerDownload").onclick = () => openPdf(pdfUrl);

    // Prefer embedded HTML from print-index (no extra fetch / no Chinese path)
    if (pr.answerHtml) {
      body.innerHTML = pr.answerHtml;
      return;
    }

    fetch(encodeURI(mdUrl) + "?v=3")
      .then((r) => {
        if (!r.ok) throw new Error("missing");
        return r.text();
      })
      .then((text) => {
        body.innerHTML = renderMd(text);
      })
      .catch(() => {
        body.innerHTML =
          "<p>在线答案暂未加载成功。</p><p class='meta'>可点下方按钮下载 A4 答案 PDF。</p>";
      });
  }

  function openGardenTips(node) {
    $("pathLessonOverlay").classList.add("hidden");
    const g = node.garden && node.garden.accumulate;
    $("answerTitle").textContent = (node.title || "语文园地") + " · 日积月累";
    let html = "";
    if (g) {
      html += "<p><b>" + (g.title || "日积月累") + "</b></p>";
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
            (it.tip ? " · " + it.tip : "") +
            "</span></p>";
        });
      }
      if (g.meaning) html += "<p><b>大意</b><br>" + g.meaning + "</p>";
      if (g.background) html += "<p class='meta'>" + g.background + "</p>";
      if (node.garden && node.garden.extra) html += "<p class='meta'>" + node.garden.extra + "</p>";
    }
    $("answerBody").innerHTML = html || "<p>暂无内容</p>";
    $("btnAnswerDownload").onclick = () => {
      const sp = state.printIndex && state.printIndex.sprint && state.printIndex.sprint[node.unitId];
      openPdf(sp);
    };
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
          const cut = Math.max(4, Math.floor(full.replace(/[，。？！、]/g, "").length / 2));
          cards.push({
            type: "write",
            title: "日积月累默写",
            prompt: "补全：" + full.slice(0, cut) + "________",
            answer: full,
            tip: it.who || g.author || "",
            meta: { moduleId, nodeId: node.id, kind: "园地默写" },
          });
        });
      } else if (moduleId === "garden_meaning") {
        const items =
          g.items ||
          g.linesDetail ||
          [{ text: (g.lines || []).join(""), tip: g.meaning }];
        items.forEach((it) => {
          cards.push({
            type: "write",
            title: "大意理解",
            prompt: "用自己的话说说意思：\n「" + (it.text || "") + "」",
            answer: it.tip || g.meaning || "意思对即可",
            tip: "参考：" + (it.tip || g.meaning || ""),
            soft: true,
            meta: { moduleId, nodeId: node.id, kind: "园地理解" },
          });
        });
      } else if (moduleId === "garden_bg") {
        cards.push({
          type: "read",
          title: "作者与背景",
          prompt: g.background || node.garden.accumulate.background || "本单元园地背景",
          answer: "",
          soft: true,
          meta: { moduleId, nodeId: node.id, kind: "背景" },
        });
      }
      return cards;
    }

    const les = node.lesson;
    if (moduleId === "words") {
      (les.words || []).forEach((w) => {
        cards.push({
          type: "write",
          title: "字词默写",
          prompt: "看拼音写词语：\n" + w.py,
          answer: w.zh,
          meta: { moduleId, nodeId: node.id, kind: "字词默写", q: w.py },
        });
      });
    } else if (moduleId === "compounds") {
      (les.compounds || []).forEach((c) => {
        cards.push({
          type: "write",
          title: "形近组词",
          prompt: "分别组词：" + c.a + "（　　）　" + c.b + "（　　）",
          answer: c.hint,
          tip: "参考：" + c.hint,
          soft: true,
          meta: { moduleId, nodeId: node.id, kind: "组词", q: c.a + "/" + c.b },
        });
      });
    } else if (moduleId === "poly") {
      (les.polyphones || []).forEach((p) => {
        cards.push({
          type: "choice",
          title: "多音字",
          prompt: "给「" + p.word + "」选正确读音",
          opts: p.opts,
          answer: p.ok,
          meta: { moduleId, nodeId: node.id, kind: "多音字", q: p.word },
        });
      });
    } else if (moduleId === "recite" && les.recite) {
      cards.push({
        type: "write",
        title: "课文默写",
        prompt: (les.recite.label || "课文默写") + "\n" + les.recite.prompt,
        answer: les.recite.answer,
        tip: "答案：" + les.recite.answer,
        meta: { moduleId, nodeId: node.id, kind: "课文默写" },
      });
    } else if (moduleId === "meaning" && les.meaning) {
      cards.push({
        type: "write",
        title: "课文大意",
        prompt: les.meaning.prompt,
        answer: les.meaning.sample,
        tip: "参考：" + les.meaning.sample,
        soft: true,
        meta: { moduleId, nodeId: node.id, kind: "课文大意" },
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
      alert("这一项还在准备内容。");
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
        : "第" + state.node.bookNo + "课 · " + state.node.title;
    $("cardType").textContent = card.title + " · " + (state.idx + 1) + "/" + total;
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
      ta.placeholder = "写在这里…";
      extra.appendChild(ta);
      const ok = document.createElement("button");
      ok.type = "button";
      ok.className = "btn-start";
      ok.textContent = "对照答案";
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
      ok.textContent = "我知道了";
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
      showFb("不对。正确：【" + card.answer + "】已计入错题。", true);
    } else {
      showFb("正确！", false);
    }
    setTimeout(() => nextCard(good), good ? 450 : 900);
  }

  function normalize(s) {
    return String(s || "")
      .replace(/\s+/g, "")
      .replace(/[，,。．.、；;：:]/g, "");
  }

  function gradeWrite(card, val) {
    if (card.soft) {
      showFb((card.tip || card.answer) + "\n（开放题：意思对即可。若完全不会可点「记错题」）", false);
      const row = document.createElement("div");
      row.className = "lesson-actions";
      const pass = document.createElement("button");
      pass.type = "button";
      pass.className = "btn-start";
      pass.textContent = "过关，下一题";
      pass.addEventListener("click", () => nextCard(true));
      const miss = document.createElement("button");
      miss.type = "button";
      miss.className = "btn-secondary";
      miss.textContent = "不会，记入错题";
      miss.addEventListener("click", () => {
        P.addMistake({
          unit: state.node.unitTitle,
          lesson: state.node.title,
          kind: card.meta.kind,
          q: card.prompt.slice(0, 40),
          wrong: val || "（空）",
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
    const parts = String(card.answer).split(/[；;、]/);
    const almost = parts.length > 1 && parts.every((p) => normalize(val).includes(normalize(p)));
    if (good || almost) {
      showFb("很好！参考：" + card.answer, false);
      setTimeout(() => nextCard(true), 500);
    } else {
      P.addMistake({
        unit: state.node.unitTitle,
        lesson: state.node.title,
        kind: card.meta.kind,
        q: card.meta.q || card.prompt.slice(0, 40),
        wrong: val || "（空）",
        right: card.answer,
      });
      state.wrong.push(card);
      showFb("再看看。正确参考：【" + card.answer + "】已计入错题。", true);
      const next = document.createElement("button");
      next.type = "button";
      next.className = "btn-start";
      next.textContent = "下一题";
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
    $("cardType").textContent = "完成";
    $("cardPrompt").textContent = "本组练习完成";
    $("cardExtra").innerHTML = "";
    $("cardFeedback").className = "feedback";
    $("cardFeedback").textContent =
      state.wrong.length === 0
        ? "全对！错题墙暂时清清爽爽。"
        : "有 " + state.wrong.length + " 处已进错题记录，可去「记录」复习。";
    const actions = $("cardActions");
    actions.innerHTML = "";
    const home = document.createElement("button");
    home.type = "button";
    home.className = "btn-start";
    home.textContent = "回主页";
    home.addEventListener("click", () => showView("home"));
    const more = document.createElement("button");
    more.type = "button";
    more.className = "btn-secondary";
    more.textContent = "继续本课其他练习";
    more.addEventListener("click", () => openNodePicker(state.node));
    actions.appendChild(home);
    actions.appendChild(more);
  }

  function renderRecords() {
    const store = P.ensure();
    $("recordsScore").innerHTML =
      "<strong>错题 " +
      (store.mistakes || []).filter((m) => m.status !== "已掌握").length +
      "</strong> 条未掌握 · 路径进度 " +
      P.completedCount() +
      "/" +
      P.semesterPath().length;

    const actions = $("recordsActions");
    actions.innerHTML = "";
    DATA.units.forEach((u) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "rec-card";
      b.innerHTML =
        "<strong>" +
        u.name.split("·")[0].trim() +
        " · 单元冲刺</strong><div class='meta' style='margin:4px 0 0'>下载冲刺 A4（测前）</div>";
      b.addEventListener("click", () => {
        const sp = state.printIndex && state.printIndex.sprint && state.printIndex.sprint[u.id];
        openPdf(sp || "printables/sprint/");
      });
      actions.appendChild(b);
      const full = document.createElement("button");
      full.type = "button";
      full.className = "rec-card";
      full.innerHTML =
        "<strong>" +
        u.name.split("·")[0].trim() +
        " · 完整摸底卷</strong><div class='meta' style='margin:4px 0 0'>学校卷数字化 PDF</div>";
      full.addEventListener("click", () => {
        const map = {
          u1: "printables/full/u01-四上第一单元练习.pdf",
          u2: "printables/full/u02-四上第二单元练习.pdf",
          u3: "printables/full/u03-四上第三单元练习-不完整.pdf",
        };
        openPdf(map[u.id]);
      });
      actions.appendChild(full);
    });
    const focus = document.createElement("button");
    focus.type = "button";
    focus.className = "rec-card";
    focus.innerHTML = "<strong>重难点练习</strong><div class='meta' style='margin:4px 0 0'>打开本单元考点练习 PDF</div>";
    focus.addEventListener("click", () => {
      const node = P.currentNode();
      const uid = node.unitId || "u2";
      openPdf("printables/weekday/practice/" + uid + "-考点练习-8至15分钟.pdf");
    });
    actions.appendChild(focus);

    const list = $("recordsList");
    list.innerHTML = "";
    const mistakes = store.mistakes || [];
    if (!mistakes.length) {
      list.innerHTML = "<p class='path-meta'>还没有错题。去做今日练习吧。</p>";
      return;
    }
    mistakes.slice(0, 40).forEach((m) => {
      const div = document.createElement("div");
      div.className = "mistake-item";
      div.innerHTML =
        "<div class='row'><strong>" +
        (m.kind || "错题") +
        "</strong><small>" +
        (m.at || "") +
        " · " +
        (m.status || "") +
        "</small></div>" +
        "<div style='margin:6px 0;font-size:.9rem'>" +
        (m.lesson || "") +
        " · " +
        (m.q || "") +
        "</div>" +
        "<div style='font-size:.85rem;color:var(--muted)'>我的：" +
        (m.wrong || "") +
        " → 正确：" +
        (m.right || "") +
        "</div>";
      const row = document.createElement("div");
      row.className = "lesson-actions";
      row.style.marginTop = "8px";
      const mastered = document.createElement("button");
      mastered.type = "button";
      mastered.className = "btn-warm";
      mastered.textContent = m.status === "已掌握" ? "已掌握" : "标为已掌握";
      mastered.addEventListener("click", () => {
        P.setMistakeStatus(m.id, "已掌握");
        renderRecords();
      });
      row.appendChild(mastered);
      div.appendChild(row);
      list.appendChild(div);
    });
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
          "-每日10分钟.pdf"
      );
    } else showView("path");
  });
  const btnAnswers = $("btnViewAnswers");
  if (btnAnswers) {
    btnAnswers.addEventListener("click", () => {
      const node = P.currentNode();
      if (node.type === "garden") openGardenTips(node);
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

  // init current lesson 8
  P.setCurrentBookLesson(DATA.currentBookLesson || 8);
  loadPrintIndex().finally(() => showView("home"));
})();
