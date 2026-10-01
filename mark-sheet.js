/* 语文书桌 · 卷面对照（红笔圈题） */
(function (g) {
  const RED_PEN = "#dc2626";
  const RED_WIDTH = 4;

  const mark = {
    pages: [],
    pageIndex: 0,
    strokes: [],
    drawing: false,
    ready: false,
  };

  function $(id) {
    return document.getElementById(id);
  }

  function markInkHasAny() {
    return mark.strokes.some((page) => page && page.length);
  }

  function setMarkHint(text, show) {
    const hint = $("markPaperHint");
    if (!hint) return;
    hint.textContent = text || "";
    hint.classList.toggle("hidden", !show);
  }

  function fitMarkCanvases(w, h) {
    const baseC = $("markBase");
    const ink = $("markInk");
    const stage = $("markStage");
    const wrap = $("markStageWrap");
    const maxW = Math.max(280, (wrap && wrap.clientWidth) || 640) - 8;
    const scale = Math.min(1, maxW / w);
    const cssW = Math.round(w * scale);
    const cssH = Math.round(h * scale);
    [baseC, ink].forEach((c) => {
      c.width = w;
      c.height = h;
      c.style.width = cssW + "px";
      c.style.height = cssH + "px";
    });
    stage.style.width = cssW + "px";
    stage.style.height = cssH + "px";
  }

  function drawMarkBase() {
    const page = mark.pages[mark.pageIndex];
    const baseC = $("markBase");
    const ctx = baseC.getContext("2d");
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, baseC.width, baseC.height);
    if (!page) return;
    ctx.drawImage(page, 0, 0, baseC.width, baseC.height);
  }

  function drawMarkInk() {
    const ink = $("markInk");
    const ctx = ink.getContext("2d");
    ctx.clearRect(0, 0, ink.width, ink.height);
    const strokes = mark.strokes[mark.pageIndex] || [];
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = RED_PEN;
    ctx.lineWidth = RED_WIDTH;
    strokes.forEach((stroke) => {
      if (!stroke || stroke.length < 2) {
        if (stroke && stroke.length === 1) {
          ctx.beginPath();
          ctx.fillStyle = RED_PEN;
          ctx.arc(stroke[0].x, stroke[0].y, RED_WIDTH / 2, 0, Math.PI * 2);
          ctx.fill();
        }
        return;
      }
      ctx.beginPath();
      ctx.moveTo(stroke[0].x, stroke[0].y);
      for (let i = 1; i < stroke.length; i++) ctx.lineTo(stroke[i].x, stroke[i].y);
      ctx.stroke();
    });
  }

  function showMarkPage() {
    const n = mark.pages.length;
    const i = mark.pageIndex;
    const prev = $("markPrevPage");
    const next = $("markNextPage");
    if (prev) prev.hidden = n <= 1;
    if (next) next.hidden = n <= 1;
    const lab = $("markPageLabel");
    if (lab) lab.textContent = n ? i + 1 + " / " + n : "";
    if (!n) return;
    const page = mark.pages[i];
    const w = page.width || page.naturalWidth || 794;
    const h = page.height || page.naturalHeight || 1123;
    fitMarkCanvases(w, h);
    drawMarkBase();
    drawMarkInk();
    setMarkHint("", false);
  }

  function inkPointFromEvent(e) {
    const ink = $("markInk");
    const rect = ink.getBoundingClientRect();
    const src = e.touches && e.touches[0] ? e.touches[0] : e;
    const x = ((src.clientX - rect.left) / rect.width) * ink.width;
    const y = ((src.clientY - rect.top) / rect.height) * ink.height;
    return { x: x, y: y };
  }

  function ensurePageStrokes() {
    while (mark.strokes.length < mark.pages.length) mark.strokes.push([]);
  }

  function bindMarkInkOnce() {
    const ink = $("markInk");
    if (!ink || ink.dataset.bound === "1") return;
    ink.dataset.bound = "1";

    const start = (e) => {
      if (!mark.ready) return;
      e.preventDefault();
      try {
        ink.setPointerCapture(e.pointerId);
      } catch (err) {
        /* ignore */
      }
      ensurePageStrokes();
      mark.drawing = true;
      const p = inkPointFromEvent(e);
      mark.strokes[mark.pageIndex].push([p]);
      drawMarkInk();
    };
    const move = (e) => {
      if (!mark.drawing) return;
      e.preventDefault();
      const strokes = mark.strokes[mark.pageIndex];
      const cur = strokes[strokes.length - 1];
      if (!cur) return;
      cur.push(inkPointFromEvent(e));
      drawMarkInk();
    };
    const end = () => {
      mark.drawing = false;
    };

    ink.addEventListener("pointerdown", start);
    ink.addEventListener("pointermove", move);
    ink.addEventListener("pointerup", end);
    ink.addEventListener("pointercancel", end);
    ink.addEventListener("pointerleave", end);
  }

  async function loadImageFromBlob(blob) {
    const url = URL.createObjectURL(blob);
    try {
      const img = new Image();
      img.decoding = "async";
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = url;
      });
      return img;
    } finally {
      URL.revokeObjectURL(url);
    }
  }

  async function renderPdfPages(url) {
    if (!g.pdfjsLib) throw new Error("pdf.js missing");
    if (!pdfjsLib.GlobalWorkerOptions.workerSrc) {
      pdfjsLib.GlobalWorkerOptions.workerSrc =
        "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";
    }
    url = String(url).replace(/\\/g, "/");
    const doc = await pdfjsLib.getDocument(encodeURI(url)).promise;
    const pages = [];
    for (let i = 1; i <= doc.numPages; i++) {
      const page = await doc.getPage(i);
      const viewport = page.getViewport({ scale: 1.35 });
      const canvas = document.createElement("canvas");
      canvas.width = Math.floor(viewport.width);
      canvas.height = Math.floor(viewport.height);
      await page.render({ canvasContext: canvas.getContext("2d"), viewport: viewport }).promise;
      pages.push(canvas);
    }
    return pages;
  }

  function paperUrlFor(printIndex, unitId, source) {
    const pi = printIndex || {};
    if (source === "sprint") return (pi.sprint && pi.sprint[unitId]) || "";
    if (source === "full") return (pi.full && pi.full[unitId]) || "";
    if (source === "garden") {
      const gg = pi.gardens && pi.gardens[unitId];
      return (gg && gg.daily) || "";
    }
    return "";
  }

  async function loadMarkPages(getPrintIndex) {
    mark.ready = false;
    mark.pages = [];
    mark.pageIndex = 0;
    mark.strokes = [];
    mark.drawing = false;
    setMarkHint("正在打开卷面…", true);

    const unitId = $("markUnit").value;
    const source = $("markSource").value;

    try {
      const url = paperUrlFor(getPrintIndex(), unitId, source);
      if (!url) throw new Error("no pdf");
      mark.pages = await renderPdfPages(url);
      mark.strokes = mark.pages.map(() => []);
      mark.ready = true;
      showMarkPage();
    } catch (err) {
      console.error(err);
      mark.pages = [];
      mark.ready = false;
      setMarkHint("卷面打不开时，可点「用照片当卷面」拍打印好的纸，再红笔圈题。", true);
    }
  }

  function openMarkSheet(opts) {
    opts = opts || {};
    if (!$("markOverlay")) return;
    bindMarkInkOnce();
    const DATA = g.CHINESE_DESK_DATA;
    const P = g.ChineseProgress;
    const sel = $("markUnit");
    sel.innerHTML = DATA.units
      .map((u) => '<option value="' + u.id + '">' + u.name + "</option>")
      .join("");
    const preferUnit =
      opts.unitId ||
      (opts.node && opts.node.unitId) ||
      (P.currentNode() && P.currentNode().unitId) ||
      "u1";
    if (preferUnit && DATA.units.some((u) => u.id === preferUnit)) sel.value = preferUnit;

    let preferSource = opts.source || "sprint";
    if (!opts.source && opts.node) {
      if (opts.node.type === "full") preferSource = "full";
      else if (opts.node.type === "garden") preferSource = "garden";
      else preferSource = "sprint";
    }
    $("markSource").value = preferSource;
    $("markMeta").textContent = "在原卷上用红笔画圈，圈完点「记上了」";
    $("markOverlay").classList.remove("hidden");
    loadMarkPages(opts.getPrintIndex || (() => null));
  }

  function undoMarkStroke() {
    ensurePageStrokes();
    const strokes = mark.strokes[mark.pageIndex];
    if (!strokes || !strokes.length) return;
    strokes.pop();
    drawMarkInk();
  }

  function clearMarkInk() {
    ensurePageStrokes();
    mark.strokes[mark.pageIndex] = [];
    drawMarkInk();
  }

  function compositeMarkedBlob() {
    return new Promise((resolve, reject) => {
      const marked = [];
      mark.pages.forEach((page, idx) => {
        if (!(mark.strokes[idx] && mark.strokes[idx].length)) return;
        marked.push(idx);
      });
      const use = marked.length ? marked : [mark.pageIndex];
      let totalH = 0;
      let maxW = 0;
      const dims = use.map((idx) => {
        const page = mark.pages[idx];
        const w = page.width || page.naturalWidth;
        const h = page.height || page.naturalHeight;
        maxW = Math.max(maxW, w);
        totalH += h + 12;
        return { idx: idx, w: w, h: h };
      });
      const out = document.createElement("canvas");
      out.width = maxW;
      out.height = Math.max(totalH - 12, 1);
      const ctx = out.getContext("2d");
      ctx.fillStyle = "#fff";
      ctx.fillRect(0, 0, out.width, out.height);
      let y = 0;
      dims.forEach((d) => {
        const page = mark.pages[d.idx];
        const tmp = document.createElement("canvas");
        tmp.width = d.w;
        tmp.height = d.h;
        const tctx = tmp.getContext("2d");
        tctx.fillStyle = "#fff";
        tctx.fillRect(0, 0, d.w, d.h);
        tctx.drawImage(page, 0, 0, d.w, d.h);
        tctx.lineCap = "round";
        tctx.lineJoin = "round";
        tctx.strokeStyle = RED_PEN;
        tctx.lineWidth = RED_WIDTH;
        (mark.strokes[d.idx] || []).forEach((stroke) => {
          if (!stroke || !stroke.length) return;
          if (stroke.length === 1) {
            tctx.beginPath();
            tctx.fillStyle = RED_PEN;
            tctx.arc(stroke[0].x, stroke[0].y, RED_WIDTH / 2, 0, Math.PI * 2);
            tctx.fill();
            return;
          }
          tctx.beginPath();
          tctx.moveTo(stroke[0].x, stroke[0].y);
          for (let i = 1; i < stroke.length; i++) tctx.lineTo(stroke[i].x, stroke[i].y);
          tctx.stroke();
        });
        ctx.drawImage(tmp, 0, y);
        y += d.h + 12;
      });
      out.toBlob(
        (blob) => (blob ? resolve(blob) : reject(new Error("blob failed"))),
        "image/jpeg",
        0.88
      );
    });
  }

  async function saveMarkSheet(sourceLabels) {
    if (!mark.ready || !mark.pages.length) {
      alert("请先打开卷面，或用照片当卷面");
      return false;
    }
    if (!markInkHasAny()) {
      alert("先用红笔在卷面上圈出错的题");
      return false;
    }
    const DB = g.ChineseMistakesDB;
    if (!DB) {
      alert("错题库未加载");
      return false;
    }
    const unitId = $("markUnit").value;
    const source = $("markSource").value;
    const labels = sourceLabels || {};
    const blob = await compositeMarkedBlob();
    await DB.putEntry({
      id: "m" + Date.now(),
      unitId: unitId,
      source: source,
      qNos: [],
      note: (labels[source] || "练习") + " · 卷面对照红笔圈题",
      status: "未掌握",
      at: new Date().toISOString().slice(0, 10),
      photoName: "mark.jpg",
      photoBlob: blob,
    });
    $("markOverlay").classList.add("hidden");
    return true;
  }

  function bindUi(getPrintIndex, onSaved) {
    const btnOpenMark = $("btnOpenMark");
    if (btnOpenMark) {
      btnOpenMark.addEventListener("click", () =>
        openMarkSheet({ getPrintIndex: getPrintIndex })
      );
    }
    const markClose = $("markClose");
    if (markClose) markClose.addEventListener("click", () => $("markOverlay").classList.add("hidden"));
    const markUnit = $("markUnit");
    if (markUnit) markUnit.addEventListener("change", () => loadMarkPages(getPrintIndex));
    const markSource = $("markSource");
    if (markSource) markSource.addEventListener("change", () => loadMarkPages(getPrintIndex));
    const markPrev = $("markPrevPage");
    if (markPrev)
      markPrev.addEventListener("click", () => {
        if (mark.pageIndex > 0) {
          mark.pageIndex -= 1;
          showMarkPage();
        }
      });
    const markNext = $("markNextPage");
    if (markNext)
      markNext.addEventListener("click", () => {
        if (mark.pageIndex < mark.pages.length - 1) {
          mark.pageIndex += 1;
          showMarkPage();
        }
      });
    const markUndo = $("markUndo");
    if (markUndo) markUndo.addEventListener("click", () => undoMarkStroke());
    const markClear = $("markClear");
    if (markClear) markClear.addEventListener("click", () => clearMarkInk());
    const markSave = $("markSave");
    if (markSave)
      markSave.addEventListener("click", () => {
        saveMarkSheet()
          .then((ok) => {
            if (ok && onSaved) onSaved();
          })
          .catch((e) => alert("保存失败：" + (e && e.message ? e.message : e)));
      });
    const markPhoto = $("markPhoto");
    if (markPhoto) {
      markPhoto.addEventListener("change", async () => {
        const file = markPhoto.files && markPhoto.files[0];
        if (!file) return;
        try {
          const img = await loadImageFromBlob(file);
          mark.pages = [img];
          mark.pageIndex = 0;
          mark.strokes = [[]];
          mark.ready = true;
          showMarkPage();
        } catch (err) {
          console.error(err);
          setMarkHint("照片打不开，请换一张再试。", true);
        }
      });
    }
  }

  g.ChineseMarkSheet = {
    open: openMarkSheet,
    bindUi: bindUi,
    paperUrlFor: paperUrlFor,
  };
})(window);
