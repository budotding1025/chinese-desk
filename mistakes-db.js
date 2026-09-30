/* 语文书桌 · 错题库（IndexedDB：照片 + 记录） */
(function (g) {
  const DB_NAME = "chinese-desk-mistakes";
  const DB_VER = 1;
  const STORE = "entries";

  function openDb() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VER);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STORE)) {
          const os = db.createObjectStore(STORE, { keyPath: "id" });
          os.createIndex("byUnit", "unitId", { unique: false });
          os.createIndex("byAt", "at", { unique: false });
          os.createIndex("byStatus", "status", { unique: false });
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  function txDone(tx) {
    return new Promise((resolve, reject) => {
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
      tx.onabort = () => reject(tx.error || new Error("aborted"));
    });
  }

  async function putEntry(entry) {
    const db = await openDb();
    const tx = db.transaction(STORE, "readwrite");
    tx.objectStore(STORE).put(entry);
    await txDone(tx);
    db.close();
    return entry;
  }

  async function deleteEntry(id) {
    const db = await openDb();
    const tx = db.transaction(STORE, "readwrite");
    tx.objectStore(STORE).delete(id);
    await txDone(tx);
    db.close();
  }

  async function listEntries() {
    const db = await openDb();
    const tx = db.transaction(STORE, "readonly");
    const req = tx.objectStore(STORE).getAll();
    const rows = await new Promise((resolve, reject) => {
      req.onsuccess = () => resolve(req.result || []);
      req.onerror = () => reject(req.error);
    });
    await txDone(tx);
    db.close();
    rows.sort((a, b) => String(b.at || "").localeCompare(String(a.at || "")) || String(b.id).localeCompare(String(a.id)));
    return rows;
  }

  async function getEntry(id) {
    const db = await openDb();
    const tx = db.transaction(STORE, "readonly");
    const req = tx.objectStore(STORE).get(id);
    const row = await new Promise((resolve, reject) => {
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
    await txDone(tx);
    db.close();
    return row;
  }

  function blobToDataUrl(blob) {
    return new Promise((resolve, reject) => {
      const fr = new FileReader();
      fr.onload = () => resolve(fr.result);
      fr.onerror = () => reject(fr.error);
      fr.readAsDataURL(blob);
    });
  }

  function dataUrlToBlob(dataUrl) {
    const parts = String(dataUrl || "").split(",");
    if (parts.length < 2) return null;
    const mime = (parts[0].match(/:(.*?);/) || [])[1] || "image/jpeg";
    const bin = atob(parts[1]);
    const arr = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
    return new Blob([arr], { type: mime });
  }

  async function exportBackup() {
    const rows = await listEntries();
    const out = [];
    for (const r of rows) {
      const item = {
        id: r.id,
        unitId: r.unitId,
        source: r.source,
        qNos: r.qNos || [],
        note: r.note || "",
        status: r.status || "未掌握",
        at: r.at,
        photoName: r.photoName || "",
      };
      if (r.photoBlob) item.photoDataUrl = await blobToDataUrl(r.photoBlob);
      out.push(item);
    }
    return {
      version: 1,
      exportedAt: new Date().toISOString(),
      entries: out,
    };
  }

  async function importBackup(payload) {
    const entries = (payload && payload.entries) || [];
    let n = 0;
    for (const e of entries) {
      const row = {
        id: e.id || "m" + Date.now() + "-" + n,
        unitId: e.unitId || "u1",
        source: e.source || "daily1",
        qNos: Array.isArray(e.qNos) ? e.qNos : [],
        note: e.note || "",
        status: e.status || "未掌握",
        at: e.at || new Date().toISOString().slice(0, 10),
        photoName: e.photoName || "",
        photoBlob: e.photoDataUrl ? dataUrlToBlob(e.photoDataUrl) : null,
      };
      await putEntry(row);
      n += 1;
    }
    return n;
  }

  g.ChineseMistakesDB = {
    putEntry,
    deleteEntry,
    listEntries,
    getEntry,
    exportBackup,
    importBackup,
    blobToDataUrl,
  };
})(window);
