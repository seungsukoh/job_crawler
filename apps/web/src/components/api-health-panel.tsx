import { useMemo, useState } from "react";

type HealthStatus = "idle" | "loading" | "ok" | "error";

type HealthPayload = {
  status?: string;
  service?: string;
  version?: string;
  environment?: string;
};

type ApiHealthPanelProps = {
  apiBaseUrl: string;
};

const statusLabels: Record<HealthStatus, string> = {
  idle: "대기",
  loading: "확인 중",
  ok: "정상",
  error: "오류",
};

export function ApiHealthPanel({ apiBaseUrl }: ApiHealthPanelProps) {
  const [status, setStatus] = useState<HealthStatus>("idle");
  const [payload, setPayload] = useState<HealthPayload | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const healthUrl = useMemo(() => {
    return `${apiBaseUrl.replace(/\/$/, "")}/health`;
  }, [apiBaseUrl]);

  async function checkHealth() {
    setStatus("loading");
    setErrorMessage(null);

    try {
      const response = await fetch(healthUrl, {
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = (await response.json()) as HealthPayload;
      setPayload(data);
      setStatus(data.status === "ok" ? "ok" : "error");
    } catch (error) {
      setPayload(null);
      setStatus("error");
      setErrorMessage(error instanceof Error ? error.message : "Unknown error");
    }
  }

  return (
    <section className="panel" aria-labelledby="health-title">
      <div className="panel-heading">
        <div>
          <p className="panel-kicker">API</p>
          <h2 id="health-title">연결 상태</h2>
        </div>
        <span className={`status-pill status-${status}`}>{statusLabels[status]}</span>
      </div>

      <div className="health-body">
        <div className="endpoint">
          <span>Endpoint</span>
          <code>{healthUrl}</code>
        </div>

        <div className="actions">
          <button
            className="primary-button"
            disabled={status === "loading"}
            onClick={checkHealth}
            type="button"
          >
            상태 확인
          </button>
        </div>

        <span className="response-label">Response</span>
        <pre className="response-box">
          {errorMessage
            ? JSON.stringify({ error: errorMessage }, null, 2)
            : JSON.stringify(payload ?? { status: "idle" }, null, 2)}
        </pre>
      </div>
    </section>
  );
}
