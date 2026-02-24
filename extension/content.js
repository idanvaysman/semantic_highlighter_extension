// content.js

console.log("Content script loaded.");

function findParagraphFromSelection(selectionObj) {
  if (!selectionObj || selectionObj.rangeCount === 0) return "";

  const range = selectionObj.getRangeAt(0);
  let node = range.commonAncestorContainer;

  // If it's a text node, move to its parent element
  if (node.nodeType === Node.TEXT_NODE) node = node.parentElement;

  // Walk up to find a reasonable container (p/article/section/div)
  while (node && node !== document.body) {
    const tag = (node.tagName || "").toLowerCase();
    if (tag === "p" || tag === "article" || tag === "section" || tag === "div") {
      const text = (node.innerText || "").trim();
      if (text) return text;
    }
    node = node.parentElement;
  }

  return "";
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_SELECTION") {
    const sel = window.getSelection();
    const highlight = sel ? sel.toString().trim() : "";
    const paragraph = findParagraphFromSelection(sel);

    sendResponse({
      highlight,
      paragraph,
      title: document.title || "",
      url: window.location.href || ""
    });
  }
});