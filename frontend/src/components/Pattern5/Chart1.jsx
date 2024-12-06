import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { CONFIG_PLOT } from "../../_constant";
import useFetch from "../../hooks/useFetch"

function Chart1() {
  const [data, setData] = useState([]);

  const [loading, makeRequest] = useFetch();
  async function fetchData() {
    const data = await makeRequest("GET", "/app/correlation");
    setData(data)
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="bg-slate-200 p-2 rounded-lg h-full">
      <Plot
        className="w-full h-full"
        data={[
          {
            type: "heatmap",
            x: data.columns,
            y: data.columns,
            z: data.values,
          },
        ]}
        layout={{
          title: "Correlation",
          margin: {
            l: 200,
            r: 200,
            b: 100,
            t: 100,
            pad: 4
          },
        }}
        config={CONFIG_PLOT}
      />
    </div>
  );
}

export default Chart1;
