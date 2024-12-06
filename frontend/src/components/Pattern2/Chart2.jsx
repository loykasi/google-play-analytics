import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import useFetch from "../../hooks/useFetch"
import { CONFIG_PLOT } from "../../_constant";

function Chart2() {
  const [apps, setApps] = useState([]);
  const [loading, makeRequest] = useFetch();

  async function fetchData() {
    const data = await makeRequest("GET", "/app/correlation-2");
    setApps(data)
  }

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="bg-slate-200 p-2 rounded-lg w-1/2">
      <Plot
        className="w-full h-[calc((100vh-94px)/2)]"
        data={[
          {
            x: apps.installs,
            y: apps.rating_5,
            type: "scattergl",
            mode: "markers",
            marker: {
              size: 10,
              opacity: 0.5,
            },
          },
        ]}
        layout={{
          title: "Thống kê giữa lượt cài đặt và đánh giá 5 sao",
          xaxis: {
            title: {
              text: "Lượt cài đặt",
            },
          },
          yaxis: {
            title: {
              text: "Đánh giá 5 sao",
            },
          },
        }}
        config={CONFIG_PLOT}
      />
    </div>
  );
}

export default Chart2;
