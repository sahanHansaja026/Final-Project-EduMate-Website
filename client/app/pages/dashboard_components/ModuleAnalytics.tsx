import { Users } from "lucide-react";

export default function ModuleAnalytics() {
    // Logic to fetch student counts would go here
    const stats = [
        { name: "ML Classification", count: 148, height: "h-36" },
        { name: "SOA Microservices", count: 94, height: "h-24" }
    ];

    return (
        <section className="border border-gray-200 rounded-xl p-6 bg-white">
            <div className="flex items-center gap-2 mb-6 text-gray-900">
                <Users size={20} />
                <h4 className="font-bold">Student Enrollment Distribution</h4>
            </div>
            <div className="flex items-end gap-4 h-48 border-b border-gray-200 pb-2">
                {stats.map((item, i) => (
                    <div key={i} className="flex-1 flex flex-col items-center gap-2">
                        <div className={`${item.height} w-full bg-gray-900 rounded-t flex items-center justify-center text-white text-xs font-bold transition-all hover:bg-gray-800`}>
                            {item.count}
                        </div>
                        <span className="text-[10px] text-gray-500 text-center font-medium uppercase">{item.name}</span>
                    </div>
                ))}
            </div>
        </section>
    );
}