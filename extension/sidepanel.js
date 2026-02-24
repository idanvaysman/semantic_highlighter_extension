// sidepanel.js

console.log("Side panel loaded.");

document.getElementById("captureBtn").addEventListener("click", async () => {
  console.log("Capture button clicked.");

  // STEP 1) get the active tab ---------
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  // STEP 2) Send message to content script in that tab ---------
  chrome.tabs.sendMessage(
    tab.id,
    { type: "GET_SELECTION" },
    (response) => {

      if (chrome.runtime.lastError) {
        console.log("SendMessage error:", chrome.runtime.lastError.message);
        return;
      }

      console.log("RAW RESPONSE:", response);
      console.log("Highlight:", response?.highlight);
      console.log("Paragraph:", response?.paragraph);
      console.log("Title:", response?.title);
      console.log("URL:", response?.url);

      if (!response || !response.highlight) {
        console.log("No highlight found");
        return;
      }

      // NORMALIZATION LAYER
      const highlight = response.highlight.trim();
      const paragraph = (response.paragraph || "").trim();

      const packet = {
        version: "1.0",
        highlight: highlight,
        paragraph: paragraph,
        title: response.title || "",
        url: response.url || "",
        timestamp: new Date().toISOString()
      };

      console.log("FULL PACKET:", packet);

      // STEP 3) Send the packet to the backend server ---------
      fetch("http://127.0.0.1:8000/capture", {

        // Use HTTP POST because we are sending new data
        method: "POST",

        // Tell the server that the body is JSON
        headers: {
          "Content-Type": "application/json"
        },

        // Convert the JavaScript object (packet) into a JSON string
        // HTTP can only send text, so we must stringify the object
        body: JSON.stringify(packet)

      })
      // When the HTTP response comes back...
      .then((res) => {

        // 'res' is the raw HTTP response object
        // It is NOT the JSON yet — we must extract the JSON body
        return res.json();  // This returns another Promise

      })
      // When the JSON parsing is finished...
      .then((data) => {

        // 'data' is now the parsed JSON sent back by FastAPI
        // Example: { status: "received", chars: 42 }
        console.log("Backend response:", data);

      })
      // If anything fails (network error, server down, CORS issue, etc.)
      .catch((err) => {

        // Log the error so we can debug what went wrong
        console.log("Fetch error:", err);

      });
    }
  );
});