"use client";

import { useState } from "react";
import axios from "axios";

type Message = {
  from: "user" | "bot";
  text: string;
};

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([
    {
      from: "bot",
      text:
        "Hi! I am your Banking Risk & Compliance Assistant. " +
        "Send a scenario and I’ll evaluate policies, KYC, fraud risk, security & final decision for you."
    }
  ]);

  const [input, setInput] = useState<string>("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMsg: Message = { from: "user", text: input };
    setMessages((prev) => [...prev, newMsg]);

    try {
      const res = await axios.post("http://127.0.0.1:8000/run-orchestrator", {
        user_input: input
      });

      const reply =
        res.data?.final_decision?.final_decision
          ? `Final Decision: ${res.data.final_decision.final_decision}
Risk: ${res.data.final_decision.final_risk_level}`
          : "I analyzed your request but couldn't get a decision.";

      setMessages((prev) => [...prev, { from: "bot", text: reply }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: "Error connecting to backend server." }
      ]);
    }

    setInput("");
  };

  return (
    <div className="w-[420px] mx-auto mt-10 shadow-2xl rounded-3xl overflow-hidden bg-white">

      {/* HEADER */}
      <div className="bg-[#6A00FF] p-5 text-white flex justify-between items-center">
        <div>
          <h2 className="font-bold text-xl">ABC AI Assistant</h2>
          <p className="text-sm text-green-300">● Online</p>
        </div>

        <button className="text-white text-xl">✖</button>
      </div>

      {/* CHAT BODY */}
      <div className="h-[420px] overflow-y-auto p-4 space-y-3 bg-gray-50 flex flex-col">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`max-w-[80%] p-3 rounded-xl text-sm leading-relaxed ${
              m.from === "bot"
                ? "bg-[#E8F5FF] text-gray-800 self-start"
                : "bg-[#EFEFEF] text-gray-900 self-end"
            }`}
          >
            {m.text}
          </div>
        ))}
      </div>

      {/* INPUT */}
      <div className="p-4 flex items-center gap-3 border-t">
        <input
          className="flex-1 border rounded-full px-4 py-2 outline-none focus:ring-2 focus:ring-purple-400"
          placeholder="Type your banking query…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />

        <button
          onClick={sendMessage}
          className="bg-[#6A00FF] text-white px-4 py-2 rounded-full hover:bg-purple-700"
        >
          ➤
        </button>
      </div>
    </div>
  );
}
