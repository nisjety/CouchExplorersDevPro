document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("promptForm");
  const loading = document.getElementById("loading");
  const messageElement = document.getElementById("message");
  const imageElement = document.getElementById("generatedImage");
  const generateButton = document.getElementById("generateButton");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Validate input
    const prompt = document.getElementById("prompt").value.trim();
    if (!prompt) {
      alert("Please enter a prompt.");
      return;
    }

    // Show loading indicator and disable button
    loading.style.display = "block";
    generateButton.disabled = true;
    generateButton.textContent = "Generating...";

    try {
      const response = await fetch(
        "https://nsironwlv8.execute-api.eu-west-1.amazonaws.com/Prod/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt }),
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageElement.textContent = result.message;
        imageElement.src = result.image_url;
        imageElement.style.display = "block";
      } else {
        messageElement.textContent = result.error || "An error occurred.";
        imageElement.style.display = "none";
      }
    } catch (error) {
      messageElement.textContent = "Failed to connect to the server.";
      imageElement.style.display = "none";
    } finally {
      // Hide loading indicator and enable button
      loading.style.display = "none";
      generateButton.disabled = false;
      generateButton.textContent = "Generate Image";
    }
  });
});
