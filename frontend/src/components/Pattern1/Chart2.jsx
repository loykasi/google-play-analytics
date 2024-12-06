import React, { useCallback, useEffect, useState } from "react";
import Select, { components } from "react-select";
import Plot from "react-plotly.js";
import { CONFIG_PLOT } from "../../_constant";
import useFetch from "../../hooks/useFetch"

const keysPie = ["rating_1", "rating_2", "rating_3", "rating_4", "rating_5"];
const labelPie = ["1 sao", "2 sao", "3 sao", "4 sao", "5 sao"];

function Chart2() {
  const [dataPie, setDataPie] = useState([]);
  const [recent, setRecent] = useState([]);
  const [options, setOptions] = useState([]);
  const [loading, makeRequest] = useFetch();

  const { Option } = components;
  const IconOption = (props) => (
    <Option {...props}>
      <div className="flex gap-2">
        <img
          className="size-10"
          src={props.data?.icon}
          alt={props.data?.label}
        />
        <div>
          <div>{props.data?.label}</div>
          <div className="text-sm">{props.data?.updated}</div>
        </div>
      </div>
    </Option>
  );

  async function fetchData() {
    const data = await makeRequest("GET", "/app/recent");
    const newData = data.map((item) => {
      return {
        value: item.id,
        label: item.title,
        icon: item.icon,
        updated: item.date,
      };
    });
    setOptions(newData);
    setRecent(data)
    console.log(data)
  }

  useEffect(() => {
    fetchData()
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

  const chooseApp = useCallback(
    (id) => {
      const find = recent.find((i) => i.id === id);
      setDataPie(keysPie.map((key) => find[key]));

      //   setDataRadar(
      //     keysPie.map(
      //       (key) =>
      //         new Object({
      //           rating: key,
      //           value: (find[key] / find.ratings) * 100,
      //         })
      //     )
      //   );
    },
    [recent]
  );

  return (
    <div className="p-2 bg-slate-200 rounded-md basis-1/3">
      <div>Những app cập nhật gần nhất</div>
      <Select
        className="mb-2"
        options={options}
        components={{ Option: IconOption }}
        onChange={(e) => {
          chooseApp(e.value);
        }}
      />
      {dataPie.every((item) => item === "0") ? (
        <div className="h-[calc(100vh-282px)] flex justify-center items-center">
          <div>Không có đánh giá</div>
        </div>
      ) : (
        <>
          <Plot
            className="w-full h-[calc(100vh-282px)]"
            data={[
              {
                values: dataPie,
                labels: labelPie,
                type: "pie",
                textposition: "inside",
              },
            ]}
            layout={{
              legend: {
                orientation: "h",
                x: 0.5,
                y: 1.1,
                xanchor: "center",
                yanchor: "bottom",
              },
              margin: {
                t: 10,
                b: 10,
                l: 10,
                r: 10,
              },
            }}
            config={CONFIG_PLOT}
          />
          {/* <RadarChart
            width={350}
            height={350}
            data={dataRadar}
            outerRadius={100}
            className="bg-white"
          >
            <PolarGrid stroke="#111" />
            <PolarAngleAxis dataKey="rating" stroke="#000" />
            <Radar
              dataKey="value"
              stroke="#8884d8"
              fill="#8884d8"
              fillOpacity={0.6}
            />
          </RadarChart> */}
        </>
      )}
    </div>
  );
}

export default Chart2;
