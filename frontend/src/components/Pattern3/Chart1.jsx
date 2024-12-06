import { useEffect, useState } from "react";
import useFetch from "../../hooks/useFetch"
import Plot from "react-plotly.js";
import { CONFIG_PLOT } from "../../_constant";

function Chart1() {
  const [data, setData] = useState([]);

  const [loading, makeRequest] = useFetch();
  async function fetchData() {
    const data = await makeRequest("GET", "/clustering/weeks");
    setData(data)
  }

  var textpositions = ['top left', 'top right', 'bottom left', 'bottom right'];  

  useEffect(() => {
    fetchData();
  }, []);

  return (<>
    {data && data.length > 0 &&
    <Plot
      className="w-full h-full"
      data={[
        {
          type: "scatter",
          x: data.map((i) => i.avg_score),
          y: data.map((i) => i.count),
          mode: "markers+text",
          marker: { size: 8 },
          transforms: [
            {
              type: "groupby",
              groups: data.map((i) => i.cluster),
            },
          ],
          text: data.map((i) => i.genre),
          textposition: data.map((i, index) => textpositions[index % textpositions.length]),
        },
      ]}
      layout={{
        title: "Thống kê danh mục",
        xaxis: { title: "Điểm số" },
        yaxis: { title: "Lượt cập nhật" },
        showlegend: true,
      }}
      config={CONFIG_PLOT}
    />
    }
  </>);
}

export default Chart1;
