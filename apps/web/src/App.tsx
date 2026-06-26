import { ApiHealthPanel } from "@/components/api-health-panel";
import { JobExplorer } from "@/components/job-explorer";
import { getApiBaseUrl } from "@/lib/config";

export function App() {
  const apiBaseUrl = getApiBaseUrl();

  return (
    <main className="page-shell">
      <div className="workspace">
        <JobExplorer apiBaseUrl={apiBaseUrl} />
        <ApiHealthPanel apiBaseUrl={apiBaseUrl} />
      </div>
    </main>
  );
}
