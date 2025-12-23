"use client";

import { useState, useEffect } from "react";
import axios from "axios";

export default function Home() {
  // =========================
  // TYPES
  // =========================
  type ResponseData = {
    final_decision: {
      final_decision: string;
      final_risk_level: string;
      decision_reasons: string[];
    };
  };

  type CustomerSuggestion = {
    customer_id: string;
    customer_name: string;
    email: string;
    kyc_status: string;
  };

  // =========================
  // STATE
  // =========================
  const [input, setInput] = useState<string>("");
  const [kycName, setKycName] = useState<string>("");

  const [response, setResponse] = useState<ResponseData | null>(null);
  const [loading, setLoading] = useState(false);

  const [suggestions, setSuggestions] = useState<CustomerSuggestion[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);

  // =========================
  // SEARCH API
  // =========================
  const searchCustomers = async (value: string) => {
    setKycName(value);

    if (value.length < 3) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }

    try {
      const res = await axios.get(
        `http://localhost:8000/search-customers?query=${value}`
      );

      setSuggestions(res.data.results || []);
      setShowDropdown(true);
    } catch {
      setSuggestions([]);
      setShowDropdown(false);
    }
  };

  // close dropdown when clicked outside
  useEffect(() => {
    const close = () => setShowDropdown(false);
    document.addEventListener("click", close);
    return () => document.removeEventListener("click", close);
  }, []);

  // =========================
  // RUN ENGINE
  // =========================
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

    const res = await axios.post(
      "http://localhost:8000/run-orchestrator",
      payload
    );

    setResponse(res.data);
    setLoading(false);
  };

  // =========================
  // COLORS
  // =========================
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "LOW":
        return "bg-green-100 text-green-700 border-green-400";
      case "MEDIUM":
        return "bg-yellow-100 text-yellow-700 border-yellow-400";
      case "HIGH":
        return "bg-red-100 text-red-700 border-red-400";
      default:
        return "bg-gray-100 text-gray-700 border-gray-400";
    }
  };

  const getDecisionColor = (decision: string) => {
    switch (decision) {
      case "ALLOW":
        return "bg-green-600";
      case "REVIEW_REQUIRED":
        return "bg-yellow-500";
      case "BLOCK":
      case "DENY":
        return "bg-red-600";
      default:
        return "bg-gray-600";
    }
  };

  return (
    <main className="min-h-screen bg-slate-100 flex justify-center items-start p-10">
      <div className="bg-white shadow-xl rounded-2xl p-10 w-[900px]">
        <h1 className="text-3xl font-bold text-blue-900 mb-6">
          ABC Bank – AI Risk & Compliance Engine
        </h1>

        {/* ================= Transaction Scenario ================= */}
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

        {/* ================= Customer Autocomplete ================= */}
        <label className="block font-semibold mb-2">
          Customer Name / Email (Search)
        </label>

        <div className="relative">
          <input
            className="w-full border p-3 rounded-lg mb-2"
            placeholder="Type at least 3 letters..."
            value={kycName}
            onChange={(e) => searchCustomers(e.target.value)}
            onClick={(e) => e.stopPropagation()}
          />

          {showDropdown && suggestions.length > 0 && (
            <div className="absolute bg-white shadow-lg rounded-lg w-full max-h-60 overflow-y-auto z-10 border">
              {suggestions.map((cust) => (
                <div
                  key={cust.customer_id}
                  className="p-3 hover:bg-blue-100 cursor-pointer border-b"
                  onClick={(e) => {
                    e.stopPropagation();
                    setKycName(cust.customer_name ?? "");
                    setSuggestions([]);
                    setShowDropdown(false);
                  }}
                >
                  <p className="font-semibold">{cust.customer_name}</p>
                  <p className="text-sm text-gray-600">{cust.email}</p>

                  <span
                    className={`text-xs px-2 py-1 rounded mt-2 inline-block ${
                      cust.kyc_status === "VALID"
                        ? "bg-green-200 text-green-900"
                        : "bg-yellow-200 text-yellow-900"
                    }`}
                  >
                    {cust.kyc_status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ================= BUTTON ================= */}
        <button
          onClick={runEngine}
          disabled={loading || !input.trim()}
          className={`px-8 py-3 rounded-lg font-semibold text-white mt-4
          ${
            loading || !input.trim()
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-red-600 hover:bg-red-700"
          }`}
        >
          {loading ? "Processing..." : "Run Compliance Check"}
        </button>

        {/* ================= USER SUMMARY ================= */}
        <div className="border border-blue-300 bg-blue-50 rounded-xl p-6 shadow-sm mt-8 mb-8">
          <h3 className="text-xl font-bold text-blue-900 mb-4">
            Banking Decision Summary
          </h3>

          {response && (
            <>
              <div className="flex items-center justify-between mb-3">
                <span className="text-gray-700 font-semibold">
                  Final Decision
                </span>
                <span
                  className={`text-white px-4 py-1 rounded-full text-sm ${getDecisionColor(
                    response.final_decision.final_decision
                  )}`}
                >
                  {response.final_decision.final_decision}
                </span>
              </div>

              <div className="flex items-center justify-between mb-5">
                <span className="text-gray-700 font-semibold">Risk Level</span>
                <span
                  className={`border px-3 py-1 rounded-full text-sm font-semibold ${getRiskColor(
                    response.final_decision.final_risk_level
                  )}`}
                >
                  {response.final_decision.final_risk_level}
                </span>
              </div>

              <div className="mt-4">
                <p className="font-semibold mb-2 text-blue-900">
                  Reason Summary
                </p>

                <ul className="list-disc pl-6 text-blue-900 leading-relaxed">
                  {response.final_decision.decision_reasons.map(
                    (r: string, index: number) => (
                      <li key={index}>{r}</li>
                    )
                  )}
                </ul>
              </div>
            </>
          )}
        </div>

        {/* ================= DEV JSON OUTPUT ================= */}
        <pre className="bg-black text-green-400 p-6 rounded-xl max-h-[450px] overflow-auto">
          {JSON.stringify(response, null, 4)}
        </pre>
      </div>
    </main>
  );
}
