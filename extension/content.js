// content.js

console.log("Content script loaded");

// Listen for messages from the side panel

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_SELECTION") {
    const selection = window.getSelection().toString();
    sendResponse({ highlight: selection });
  }
});