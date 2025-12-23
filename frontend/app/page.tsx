"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [input, setInput] = useState("");
  const [kycName, setKycName] = useState("");
  const [response, setResponse] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);

  const runEngine = async () => {
    setLoading(true);
    setResponse(null);

    const payload = {
      user_input: input,
      kyc_data: {
        customer_name: kycName || "Test User",
        kyc_status: "VALID",
        nationality: "India",
      },
      memory: [],
    };

    const res = await axios.post("http://localhost:8000/run-orchestrator", payload);

    setResponse(res.data);
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-slate-100 flex justify-center items-start p-10">
      <div className="bg-white shadow-xl rounded-2xl p-10 w-[900px]">
        <h1 className="text-3xl font-bold text-blue-900 mb-6">
          ABC Bank – AI Risk & Compliance Engine
        </h1>

        <label className="block font-semibold mb-2">
          Banking Transaction Scenario
        </label>
        <textarea
          className="w-full border p-3 rounded-lg mb-6"
          rows={4}
          placeholder="Example: Customer transferring $15,000 to new beneficiary..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />

        <label className="block font-semibold mb-2">
          Customer Name (Optional)
        </label>
        <input
          className="w-full border p-3 rounded-lg mb-6"
          placeholder="Balbir Kaur"
          value={kycName}
          onChange={(e) => setKycName(e.target.value)}
        />

        <button
          onClick={runEngine}
          disabled={loading || !input.trim()}
          className={`px-8 py-3 rounded-lg font-semibold text-white 
    ${
      loading || !input.trim()
        ? "bg-gray-400 cursor-not-allowed"
        : "bg-red-600 hover:bg-red-700"
    }`}
        >
          {loading ? "Processing..." : "Run Compliance Check"}
        </button>

        {response && (
          <div className="mt-8">
            <h2 className="text-xl font-bold mb-4 text-green-700">
              Final Decision & Results
            </h2>

            <pre className="bg-black text-green-400 p-6 rounded-xl max-h-[450px] overflow-auto">
              {JSON.stringify(response, null, 4)}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
}
