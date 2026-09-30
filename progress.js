/* 语文书桌 · 进度 / 错题 / 当前课 */
(function (g) {
  const KEY = "chinese-desk-v1";
  const DATA = g.CHINESE_DESK_DATA;

  function load() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || "{}") || {};
    } catch (e) {
      return {};
    }
  }

  function save(store) {
    localStorage.setItem(KEY, JSON.stringify(store));
  }

  function ensure() {
    const s = load();
    if (!s.completed) s.completed = {};
    if (!s.mistakes) s.mistakes = [];
    if (!s.streak) s.streak = { count: 0, last: "" };
    if (!s.currentBookLesson) s.currentBookLesson = DATA.currentBookLesson || 8;
    return s;
  }

  function semesterPath() {
    const nodes = [];
    (DATA.units || []).forEach((u) => {
      (u.lessons || []).forEach((les) => {
        nodes.push({
          type: "lesson",
          id: les.id,
          unitId: u.id,
          unitTitle: u.name,
          bookNo: les.bookNo,
          title: les.title,
          kind: les.kind,
          lesson: les,
        });
      });
      if (u.garden) {
        nodes.push({
          type: "garden",
          id: u.garden.id,
          unitId: u.id,
          unitTitle: u.name,
          bookNo: null,
          title: u.garden.title,
          kind: "园地",
          garden: u.garden,
        });
      }
    });
    return nodes;
  }

  function nodeByBookLesson(n) {
    return semesterPath().find((x) => x.type === "lesson" && x.bookNo === n) || null;
  }

  function nodeById(id) {
    return semesterPath().find((x) => x.id === id) || null;
  }

  function currentNode() {
    const s = ensure();
    return nodeByBookLesson(s.currentBookLesson) || nodeByBookLesson(DATA.currentBookLesson) || semesterPath()[0];
  }

  function markDone(nodeId, moduleId) {
    const s = ensure();
    if (!s.completed[nodeId]) s.completed[nodeId] = { modules: {}, count: 0 };
    s.completed[nodeId].modules[moduleId] = Date.now();
    s.completed[nodeId].count = Object.keys(s.completed[nodeId].modules).length;
    const today = new Date().toISOString().slice(0, 10);
    if (s.streak.last !== today) {
      const y = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
      s.streak.count = s.streak.last === y ? (s.streak.count || 0) + 1 : 1;
      s.streak.last = today;
    }
    save(s);
    return s;
  }

  function addMistake(entry) {
    const s = ensure();
    s.mistakes.unshift(
      Object.assign(
        {
          id: "m" + Date.now(),
          at: new Date().toISOString().slice(0, 10),
          status: "未掌握",
        },
        entry
      )
    );
    if (s.mistakes.length > 200) s.mistakes.length = 200;
    save(s);
    return s;
  }

  function setMistakeStatus(id, status) {
    const s = ensure();
    const m = (s.mistakes || []).find((x) => x.id === id);
    if (m) m.status = status;
    save(s);
    return s;
  }

  function setCurrentBookLesson(n) {
    const s = ensure();
    s.currentBookLesson = n;
    save(s);
    return s;
  }

  function completedCount() {
    const s = ensure();
    return semesterPath().filter((n) => s.completed[n.id] && s.completed[n.id].count > 0).length;
  }

  g.ChineseProgress = {
    ensure,
    save,
    load,
    semesterPath,
    nodeById,
    nodeByBookLesson,
    currentNode,
    markDone,
    addMistake,
    setMistakeStatus,
    setCurrentBookLesson,
    completedCount,
  };
})(window);
