const express = require("express");
const cors = require("cors");
const { Client } = require("gradio-client");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const HF_TOKEN = process.env.HF_API_TOKEN;
const client = new Client("chandubram/chandan-private-chatbot", {
  hf_token: HF_TOKEN,
});

app.post("/api/chat", async (req, res) => {
  try {
    const { message, history = [] } = req.body;

    const result = await client.predict(
      message,
      history,
      "You are Chandan-Bot, a formal and professional assistant. Answer ONLY based on the provided data and never generate information outside of it. If the information is not available, say: 'I'm sorry, but I do not have that information.' Always speak in the first person.",
      512,
      0.7,
      0.95,
      "/chat"
    );

    res.json({ reply: result });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to contact AI backend." });
  }
});

app.listen(PORT, () => {
  console.log(`Proxy server running on port ${PORT}`);
});
