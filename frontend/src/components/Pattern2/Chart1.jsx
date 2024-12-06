import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import useFetch from "../../hooks/useFetch"
import { CONFIG_PLOT } from "../../_constant";

function Chart1() {
  const [loading, makeRequest] = useFetch();
  const [scoreHistogram, setScoreHistogram] = useState(null);

  async function fetchData() {
    const data = await makeRequest("GET", "/app/histogram/score");
    setScoreHistogram(data)
  }

  useEffect(() => {
    fetchData()
  }, []);
  return (
    <div className="bg-slate-200 p-2 rounded-lg w-1/2">
      {scoreHistogram &&
      <Plot
        className="w-full h-[calc((100vh-94px)/2)]"
        data={[
          {
            x: scoreHistogram.bins,
            y: scoreHistogram.hist,
            type: "bar",
            mode: "lines+markers+text",
            // text: scoreHistogram.hist,
            // textposition: "auto",
          },
        ]}
        layout={{ title: "Biểu đồ điểm số", dragmode: "pan" }}
        style={{ width: "100%" }}
        config={CONFIG_PLOT}
      />
      }
    </div>
  );
}

export default Chart1;
