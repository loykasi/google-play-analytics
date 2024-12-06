import Chart1 from "../components/Pattern2/Chart1";
import Chart2 from "../components/Pattern2/Chart2";
import Chart3 from "../components/Pattern2/Chart3";

function Pattern2() {
  return (
    <div className="p-4">
      <div className="rounded-lg flex gap-4">
        <Chart1 />

        <Chart2 />
      </div>

      <Chart3 />
    </div>
  );
}

export default Pattern2;
