// sidepanel.js

console.log("Side panel loaded.");

document.getElementById("captureBtn").addEventListener("click", async () => {
  console.log("Capture button clicked.");

  // Get the currently active tab
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  // Send message to content script in that tab
  chrome.tabs.sendMessage(
    tab.id,
    { type: "GET_SELECTION" },
    (response) => {
      // prints the response from content script
        console.log("RAW RESPONSE", response);
    // extra logs
        console.log("Highlight:", response?.highlight);
        console.log("Paragraph:", response?.paragraph);
        console.log("Title:", response?.title);
        console.log("URL:", response?.url);
    }
  );
});