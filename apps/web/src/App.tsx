import { ApiHealthPanel } from "@/components/api-health-panel";
import { JobExplorer } from "@/components/job-explorer";
import { getApiBaseUrl, shouldUseStaticJobData } from "@/lib/config";

export function App() {
  const apiBaseUrl = getApiBaseUrl();
  const useStaticJobData = shouldUseStaticJobData();

  return (
    <main className="page-shell">
      <div className="workspace">
        <JobExplorer apiBaseUrl={apiBaseUrl} useStaticJobData={useStaticJobData} />
        <ApiHealthPanel apiBaseUrl={apiBaseUrl} />
      </div>
    </main>
  );
}
