import Chart2 from "../components/Pattern4/Chart2";
import Chart1 from "../components/Pattern4/Chart1";

function Pattern4() {
  return (
    <div className="p-5 h-screen">
      <div className="text-center text-xl mb-4">
        Thống kê top danh mục 7 ngày vừa qua
      </div>
      <div className="bg-slate-200 p-2 flex gap-2 h-[calc(100vh-100px)]">
        <Chart1 />
        <Chart2 />
      </div>
    </div>
  );
}

export default Pattern4;
