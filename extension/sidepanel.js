// sidepanel.js

console.log("Side panel loaded.");

let pendingRankPromise = null;

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
      
      const searchPromise = fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(packet)
      }).then((res) => res.json());

      pendingRankPromise = searchPromise.then(searchData => {
        console.log("Search complete, starting background rank with search results...");
        return fetch("http://127.0.0.1:8000/rank", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(searchData) 
        }).then(res => res.json());
      });

      searchPromise.then((data) => {
        console.log("Backend response (Search):", data);

        const resultsContainer = document.getElementById("results");

        if (!resultsContainer) {
          console.log("No results container found in HTML.");
          return;
        }

        resultsContainer.innerHTML = "";

        if (!data.papers || data.papers.length === 0) {
          resultsContainer.innerHTML = "<p>No articles found.</p>";
          return;
        }

        renderPapersList(data.papers);

        const analyzeBar = document.getElementById("analyzeBar");
        if (analyzeBar) analyzeBar.style.display = "flex";

      })
      .catch((err) => {
        console.log("Fetch error (Search):", err);
      });
    }
  );
});

function renderPapersList(papers) {
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = "";

  if (!papers || !Array.isArray(papers)) {
    console.log("Error: 'papers' is not a valid list", papers);
    return;
  }

  papers.forEach((paper) => {
    const paperDiv = document.createElement("div");
    // Removed borderBottom from here as requested
    paperDiv.style.marginBottom = "8px"; 
    paperDiv.style.paddingBottom = "4px";

    const title = document.createElement("div");
    title.textContent = paper.title || "Untitled";
    title.style.fontWeight = "bold";
    title.style.fontSize = "14px";
    title.style.color = "white";

    const year = document.createElement("div");
    year.textContent = paper.year || "";
    year.style.fontSize = "12px";
    year.style.color = "rgba(255, 255, 255, 0.6)";

    const link = document.createElement("a");
    link.href = paper.url;
    link.textContent = "View Paper";
    link.target = "_blank";
    // Using your darker indigo for better legibility
    link.style.color = "#4338ca"; 

    paperDiv.appendChild(title);
    paperDiv.appendChild(year);
    paperDiv.appendChild(link);

    // THE LINE: Placed strictly AFTER the content
    const line = document.createElement("div");
    // Changed to rgba for a better "Glass" look consistent with your theme
    line.style.borderBottom = "1px solid rgba(255, 255, 255, 0.2)"; 
    line.style.marginTop = "12px";
    line.style.marginBottom = "20px"; 

    resultsContainer.appendChild(paperDiv);
    resultsContainer.appendChild(line);
  });
}

// Updated Animation Logic inside DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  const bar = document.getElementById("analyzeBar");
  const star = document.getElementById("aiStar");
  const label = document.getElementById("aiLabel");

  if (bar) bar.style.display = "none";

  bar.addEventListener("click", () => {
    if (!pendingRankPromise) return;

    label.textContent = "Analyzing papers...";
    
    // Reset state and start acceleration
    star.classList.remove("spin-stop", "spin-loop", "spin-none");
    star.classList.add("spin-start");

    pendingRankPromise.then((rankData) => {
      // Switch to constant fast loop after acceleration finishes
      setTimeout(() => {
        star.classList.remove("spin-start");
        star.classList.add("spin-loop");
      }, 1000);

      setTimeout(() => {
        // STOP: Remove spinning and add the landing animation
        star.classList.remove("spin-start", "spin-loop");
        star.classList.add("spin-stop");
        
        renderPapersList(rankData.papers);
        label.textContent = "AI Analysis Complete";
      }, 2000); // Slightly longer to let the user feel the "work"
    }).catch(err => {
      console.log("Rank Error:", err);
      star.classList.add("spin-none");
    });
  });
});