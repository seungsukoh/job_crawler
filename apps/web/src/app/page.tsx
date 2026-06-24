import { ApiHealthPanel } from "@/components/api-health-panel";
import { getApiBaseUrl } from "@/lib/config";

const buildLanes = [
  { label: "API", value: "FastAPI /health 준비" },
  { label: "Web", value: "Next.js 기본 앱" },
  { label: "Data", value: "PostgreSQL 예정" },
  { label: "Crawler", value: "Source Registry 이후" },
];

export default function HomePage() {
  const apiBaseUrl = getApiBaseUrl();

  return (
    <main className="page-shell">
      <section className="workspace">
        <div className="heading-block">
          <p className="eyebrow">Job Crawler</p>
          <h1>채용 공고 탐색 작업대</h1>
          <p className="summary">
            직무 키워드와 마감일 기준의 공고 탐색 경험을 작게 검증하기 위한 MVP 화면입니다.
          </p>
        </div>

        <div className="grid">
          <ApiHealthPanel apiBaseUrl={apiBaseUrl} />

          <section className="panel" aria-labelledby="lane-title">
            <div className="panel-heading">
              <p className="panel-kicker">Build lanes</p>
              <h2 id="lane-title">작업 경계</h2>
            </div>
            <div className="lane-list">
              {buildLanes.map((lane) => (
                <div className="lane" key={lane.label}>
                  <span>{lane.label}</span>
                  <strong>{lane.value}</strong>
                </div>
              ))}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
