import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { CONFIG_PLOT } from "../../_constant";
import useFetch from "../../hooks/useFetch"

function Chart1() {
  const [dataApp, setDataApp] = useState([]);

  const [loading, makeRequest] = useFetch();
  async function fetchData() {
    const data = await makeRequest("GET", "/group/genre/app/30");
    setDataApp(data)
  }
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Plot
      className="w-full h-full"
      data={[
        {
          type: "bar",
          y: dataApp.map((i) => i.genre),
          x: dataApp.map((i) => i.count),
          text: dataApp.map((i) => i.count),
          textposition: "top",
          orientation: "h",
        },
      ]}
      layout={{
        title: "Ứng dụng",
        xaxis: { title: "Lượt cập nhật" },
        yaxis: {
          ticklabelposition: "inside",
          autorange: "reversed"
        },
      }}
      config={CONFIG_PLOT}
    />
  );
}

export default Chart1;
