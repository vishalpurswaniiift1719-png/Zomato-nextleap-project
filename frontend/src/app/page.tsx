"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [locations, setLocations] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  
  // Form State
  const [location, setLocation] = useState("");
  const [budget, setBudget] = useState("medium");
  const [cuisineStr, setCuisineStr] = useState("");
  const [preferences, setPreferences] = useState("");
  const [minRating, setMinRating] = useState(3.0);
  
  // Results State
  const [results, setResults] = useState<any[]>([]);
  const [error, setError] = useState("");

  // Safely get API URL and remove trailing slash if user added it by mistake
  const getApiUrl = () => {
    let url = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    if (url.endsWith("/")) url = url.slice(0, -1);
    return url;
  };

  useEffect(() => {
    const apiUrl = getApiUrl();
    fetch(`${apiUrl}/api/locations`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to connect to backend API");
        return res.json();
      })
      .then((data) => {
        if (data.locations && data.locations.length > 0) {
          setLocations(data.locations);
          setLocation(data.locations[0]);
        }
      })
      .catch((err) => {
        console.error("Error fetching locations:", err);
        setError(`Cannot connect to Backend (${apiUrl}). Did you redeploy Vercel with the env variable?`);
      });
  }, []);

  const handleSearch = async () => {
    if (!location) {
      setError("Please wait for locations to load from the server.");
      return;
    }
    setLoading(true);
    setError("");
    setResults([]);

    try {
      const apiUrl = getApiUrl();
      const cuisinesList = cuisineStr
        .split(",")
        .map((c) => c.trim())
        .filter((c) => c.length > 0);

      const response = await fetch(`${apiUrl}/api/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          location: location,
          budget: budget,
          cuisines: cuisinesList,
          min_rating: minRating,
          preferences: preferences,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch recommendations (${response.status})`);
      }

      const data = await response.json();
      setResults(data.recommendations || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex w-full">
      <aside className="hidden md:flex bg-surface/60 backdrop-blur-xl fixed left-0 top-0 h-full w-[280px] border-r border-white/5 shadow-xl flex-col py-2 z-40 transition-transform">
        <div className="px-6 py-6 border-b border-white/5 mb-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full overflow-hidden bg-surface-container border border-white/10 shrink-0 flex items-center justify-center bg-primary/20 text-primary">
            <span className="material-symbols-outlined">restaurant</span>
          </div>
          <div>
            <h1 className="font-headline-md text-[24px] leading-8 font-bold text-primary truncate">
              Nocturne Dining
            </h1>
            <p className="font-label-md text-[14px] text-on-surface-variant truncate">
              AI Concierge
            </p>
          </div>
        </div>

        <div className="px-6 py-6 border-t border-white/5 overflow-y-auto">
          <h3 className="font-label-md text-[14px] text-on-surface-variant mb-4 uppercase tracking-wider">
            Search Filters
          </h3>
          <div className="space-y-5">
            <div>
              <label className="block font-label-md text-[14px] text-on-surface mb-2">
                Neighborhood / Location
              </label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm">
                  location_city
                </span>
                <select
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full bg-surface-container border-white/10 text-on-surface rounded-lg pl-10 pr-4 py-2 font-body-md text-[16px] focus:border-primary focus:ring-1 focus:ring-primary appearance-none transition-colors"
                >
                  {locations.map((loc) => (
                    <option key={loc} value={loc}>
                      {loc}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block font-label-md text-[14px] text-on-surface mb-2">
                Budget
              </label>
              <div className="flex gap-2">
                {["low", "medium", "high"].map((b) => (
                  <button
                    key={b}
                    onClick={() => setBudget(b)}
                    className={"flex-1 py-1.5 rounded-full border font-label-sm text-[12px] capitalize transition-all " + (budget === b ? "border-primary bg-primary/10 text-primary" : "border-white/10 bg-surface-container text-on-surface-variant hover:border-primary hover:text-primary")}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block font-label-md text-[14px] text-on-surface mb-2">
                Cuisine (Comma separated)
              </label>
              <input
                type="text"
                value={cuisineStr}
                onChange={(e) => setCuisineStr(e.target.value)}
                placeholder="e.g. Chinese, Italian"
                className="w-full bg-surface-container border-white/10 text-on-surface rounded-lg px-3 py-2 font-body-md text-[16px] focus:border-primary focus:ring-1 focus:ring-primary placeholder-on-surface-variant"
              />
            </div>

            <div>
              <label className="block font-label-md text-[14px] text-on-surface mb-2 flex justify-between">
                <span>Minimum Rating</span>
                <span className="text-primary font-bold">{minRating}</span>
              </label>
              <input
                type="range"
                min="0"
                max="5"
                step="0.1"
                value={minRating}
                onChange={(e) => setMinRating(parseFloat(e.target.value))}
                className="w-full accent-primary h-2 bg-surface-container rounded-lg appearance-none cursor-pointer"
              />
            </div>

            <div>
              <label className="block font-label-md text-[14px] text-on-surface mb-2">
                Describe your vibe
              </label>
              <textarea
                value={preferences}
                onChange={(e) => setPreferences(e.target.value)}
                className="w-full bg-surface-container border-white/10 text-on-surface rounded-lg px-3 py-2 font-body-md text-[16px] focus:border-primary focus:ring-1 focus:ring-primary placeholder-on-surface-variant resize-none h-20 transition-colors"
                placeholder="e.g. Intimate, low lighting, romantic date night..."
              ></textarea>
            </div>
          </div>

          <button
            onClick={handleSearch}
            disabled={loading}
            className={"w-full mt-6 bg-gradient-to-r from-primary-container to-tertiary-container text-white font-label-md text-[14px] py-3 rounded-lg font-semibold transition-opacity flex items-center justify-center gap-2 group " + (loading ? "opacity-50" : "btn-glow hover:opacity-90")}
          >
            {loading ? (
              <span className="material-symbols-outlined animate-spin text-sm">
                refresh
              </span>
            ) : (
              <span className="material-symbols-outlined text-sm group-hover:animate-pulse">
                auto_awesome
              </span>
            )}
            {loading ? "Searching..." : "Find Recommendations"}
          </button>
        </div>
      </aside>

      <main className="md:ml-[280px] w-full pt-12 pb-12 px-6 min-h-screen">
        <div className="max-w-5xl mx-auto mb-12 text-center md:text-left">
          <h2 className="font-display-lg text-[48px] leading-[56px] font-bold mb-4">
            Curated for you by <br />
            <span className="text-gradient">Your AI Dining Assistant</span>
          </h2>
          <p className="font-body-lg text-[18px] text-on-surface-variant max-w-2xl">
            {preferences ? "Based on your preference for: " + preferences : "Tell me what you are looking for in the sidebar, and I will find the perfect spot."}
          </p>
        </div>

        {error && (
          <div className="max-w-5xl mx-auto mb-6 p-4 bg-error-container text-on-error-container rounded-xl border border-error">
            <p className="font-body-md">Error: {error}</p>
          </div>
        )}

        {loading && (
          <div className="max-w-5xl mx-auto text-center py-20">
            <span className="material-symbols-outlined animate-spin text-[48px] text-primary">
              sync
            </span>
            <p className="mt-4 text-on-surface-variant font-body-lg">
              Analyzing the dataset with AI...
            </p>
          </div>
        )}

        {!loading && !error && results.length === 0 && (
          <div className="max-w-5xl mx-auto text-center py-20 border border-dashed border-white/20 rounded-xl">
            <span className="material-symbols-outlined text-[48px] text-on-surface-variant mb-4">
              search_off
            </span>
            <p className="text-on-surface-variant font-body-lg">
              No recommendations found yet. Try adjusting your filters or hitting Search!
            </p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <div className="max-w-5xl mx-auto flex flex-col gap-4">
            {results.map((rec, index) => (
              <article
                key={rec.name}
                className={"glass-panel rounded-xl overflow-hidden flex flex-col md:flex-row group relative " + (index === 0 ? "p-8 border-primary/30" : "p-6")}
              >
                <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>

                <div className="flex-1 flex flex-col relative z-10">
                  <div className="flex justify-between items-start mb-2">
                    <h3
                      className={"font-bold text-on-surface group-hover:text-primary transition-colors " + (index === 0 ? "font-headline-lg text-[32px]" : "font-headline-md text-[24px]")}
                    >
                      <span className="text-primary-fixed-dim mr-2">
                        #{rec.rank}
                      </span>
                      {rec.name}
                    </h3>
                    <div className="flex items-center gap-1 text-tertiary">
                      <span className="material-symbols-outlined text-sm">
                        star
                      </span>
                      <span className="font-label-md font-bold">{rec.rating}</span>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 mb-6">
                    <span className="px-2 py-1 rounded bg-secondary-container/30 text-secondary font-label-sm text-[12px]">
                      {rec.cuisines || "Various"}
                    </span>
                    <span className="px-2 py-1 rounded bg-surface-container text-on-surface-variant font-label-sm text-[12px]">
                      ₹{rec.cost} for two
                    </span>
                    <span className="px-2 py-1 rounded bg-surface-container text-on-surface-variant font-label-sm text-[12px] flex items-center gap-1">
                      <span className="material-symbols-outlined text-[14px]">location_on</span>
                      {rec.location}
                    </span>
                  </div>

                  <div
                    className={"mt-auto border rounded-xl p-4 " + (index === 0 ? "bg-primary/5 border-primary/20" : "bg-surface-container-high border-white/5")}
                  >
                    <div className="flex items-center gap-2 mb-2 text-primary-fixed-dim">
                      <span className="material-symbols-outlined text-sm">
                        {index === 0 ? "auto_awesome" : "lightbulb"}
                      </span>
                      <span className="font-label-md text-[14px] font-bold">
                        AI Reason
                      </span>
                    </div>
                    <p className="font-body-md text-[16px] text-on-surface-variant italic">
                      "{rec.reason}"
                    </p>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
