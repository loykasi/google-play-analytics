import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import { CONFIG_PLOT } from "../../_constant";
import useFetch from "../../hooks/useFetch"

function Chart1() {
  const [showChart, setShowChart] = useState(0);
  const [updatedHour, setUpdatedHour] = useState([]);

  const [loading, makeRequest] = useFetch();
  async function fetchData() {
    const data = await makeRequest("GET", "/group/hour/24");
    setUpdatedHour(data)
  }

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    let ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onmessage = e => {
      const message = JSON.parse(e.data);
      
      if (message.type === "refresh") {
        fetchData();
      }
    };

    return () => {
      ws.close();
    }
  })

  return (
    <div className="bg-slate-200 p-2 rounded-lg basis-2/3 h-fit">
      {updatedHour.length > 0 && 
      <Plot
        className="w-full h-[calc(100vh-232px)]"
        data={[
          {
            x: updatedHour.map((item) => item.date_hour),
            y: updatedHour.map((item) => item.updated),
            text: updatedHour.map((item) => item.updated).map(String),
            textposition: "auto",
            type: "bar",
          },
        ]}
        layout={{
          title: "Cập nhật trong những giờ gần đây",
          xaxis: {
            fixedrange: true,
          },
        }}
        config={CONFIG_PLOT}
      />
      }
    </div>
  );
}

export default Chart1;
