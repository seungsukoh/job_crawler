import { useEffect, useMemo, useState } from "react";

import { buildJobsUrl, listStaticJobs, type Job, type JobsResponse } from "@/lib/jobs";

type JobExplorerProps = {
  apiBaseUrl: string;
  useStaticJobData: boolean;
};

const savedJobsStorageKey = "job_crawler.saved_jobs.v1";

const statusLabels: Record<string, string> = {
  active: "진행 중",
  closed: "마감",
  deadline_unknown: "마감 미정",
};

const employmentLabels: Record<string, string> = {
  conversion_intern: "채용연계형",
  entry_level: "신입",
  intern: "인턴",
  part_time: "파트타임",
};

export function JobExplorer({ apiBaseUrl, useStaticJobData }: JobExplorerProps) {
  const [keyword, setKeyword] = useState("");
  const [deadlineFrom, setDeadlineFrom] = useState("");
  const [deadlineTo, setDeadlineTo] = useState("");
  const [includeClosed, setIncludeClosed] = useState(false);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
  const [savedJobIds, setSavedJobIds] = useState<string[]>([]);
  const [dataSource, setDataSource] = useState<string>(
    useStaticJobData ? "sample-static" : "sample",
  );
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const selectedJob = useMemo(() => {
    return jobs.find((job) => job.id === selectedJobId) ?? jobs[0] ?? null;
  }, [jobs, selectedJobId]);

  const savedJobSet = useMemo(() => new Set(savedJobIds), [savedJobIds]);

  useEffect(() => {
    const savedValue = window.localStorage.getItem(savedJobsStorageKey);
    if (!savedValue) {
      return;
    }

    try {
      const parsedValue = JSON.parse(savedValue);
      if (Array.isArray(parsedValue)) {
        setSavedJobIds(parsedValue.filter((item): item is string => typeof item === "string"));
      }
    } catch {
      setSavedJobIds([]);
    }
  }, []);

  useEffect(() => {
    void loadJobs({
      keyword,
      deadlineFrom,
      deadlineTo,
      includeClosed,
    });
    // Run once on mount. User-driven filtering calls loadJobs directly.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function loadJobs(query: {
    keyword: string;
    deadlineFrom: string;
    deadlineTo: string;
    includeClosed: boolean;
  }) {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      if (useStaticJobData) {
        applyJobsResponse(listStaticJobs(query));
        return;
      }

      const response = await fetch(
        buildJobsUrl(apiBaseUrl, {
          keyword: query.keyword,
          deadlineFrom: query.deadlineFrom,
          deadlineTo: query.deadlineTo,
          includeClosed: query.includeClosed,
        }),
        {
          headers: {
            Accept: "application/json",
          },
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const payload = (await response.json()) as JobsResponse;
      applyJobsResponse(payload);
    } catch (error) {
      applyJobsResponse(listStaticJobs(query));
      const message = error instanceof Error ? error.message : "Unknown error";
      setErrorMessage(`API unavailable; showing built-in sample data. (${message})`);
    } finally {
      setIsLoading(false);
    }
  }

  function applyJobsResponse(payload: JobsResponse) {
    setJobs(payload.items);
    setDataSource(payload.data_source);
    setSelectedJobId((currentId) => {
      if (currentId && payload.items.some((job) => job.id === currentId)) {
        return currentId;
      }
      return payload.items[0]?.id ?? null;
    });
  }

  function resetFilters() {
    setKeyword("");
    setDeadlineFrom("");
    setDeadlineTo("");
    setIncludeClosed(false);
  }

  function toggleSaved(jobId: string) {
    setSavedJobIds((currentIds) => {
      const nextIds = currentIds.includes(jobId)
        ? currentIds.filter((currentId) => currentId !== jobId)
        : [...currentIds, jobId];
      window.localStorage.setItem(savedJobsStorageKey, JSON.stringify(nextIds));
      return nextIds;
    });
  }

  return (
    <section className="job-workspace" aria-labelledby="jobs-title">
      <header className="workspace-header">
        <div>
          <p className="eyebrow">Jobs</p>
          <h1 id="jobs-title">공고 탐색</h1>
        </div>
        <div className="metric-row" aria-label="공고 요약">
          <Metric label="표시" value={`${jobs.length}`} />
          <Metric label="저장" value={`${savedJobIds.length}`} />
          <Metric label="데이터" value={dataSource} />
        </div>
      </header>

      <form
        className="filter-bar"
        onSubmit={(event) => {
          event.preventDefault();
          void loadJobs({
            keyword,
            deadlineFrom,
            deadlineTo,
            includeClosed,
          });
        }}
      >
        <label className="filter-field filter-keyword">
          <span>직무 키워드</span>
          <input
            onChange={(event) => setKeyword(event.target.value)}
            placeholder="python, frontend, data"
            type="search"
            value={keyword}
          />
        </label>

        <label className="filter-field">
          <span>시작 마감일</span>
          <input
            onChange={(event) => setDeadlineFrom(event.target.value)}
            type="date"
            value={deadlineFrom}
          />
        </label>

        <label className="filter-field">
          <span>종료 마감일</span>
          <input
            onChange={(event) => setDeadlineTo(event.target.value)}
            type="date"
            value={deadlineTo}
          />
        </label>

        <label className="toggle-field">
          <input
            checked={includeClosed}
            onChange={(event) => setIncludeClosed(event.target.checked)}
            type="checkbox"
          />
          <span>마감 포함</span>
        </label>

        <div className="filter-actions">
          <button
            className="secondary-button"
            onClick={() => {
              resetFilters();
              void loadJobs({
                keyword: "",
                deadlineFrom: "",
                deadlineTo: "",
                includeClosed: false,
              });
            }}
            type="button"
          >
            초기화
          </button>
          <button className="primary-button" disabled={isLoading} type="submit">
            {isLoading ? "조회 중" : "조회"}
          </button>
        </div>
      </form>

      {errorMessage ? <p className="error-banner">{errorMessage}</p> : null}

      <div className="jobs-grid">
        <div className="job-list" aria-label="공고 목록">
          {jobs.map((job) => (
            <button
              className={`job-row ${selectedJob?.id === job.id ? "job-row-selected" : ""}`}
              key={job.id}
              onClick={() => setSelectedJobId(job.id)}
              type="button"
            >
              <span className="job-row-main">
                <strong>{job.title}</strong>
                <span>{job.company}</span>
              </span>
              <span className="job-row-meta">
                <Badge>{statusLabels[job.status] ?? job.status}</Badge>
                <span>{formatDeadline(job.deadline)}</span>
              </span>
            </button>
          ))}

          {!isLoading && jobs.length === 0 ? (
            <div className="empty-state">
              <strong>표시할 공고가 없습니다.</strong>
              <span>검색어나 마감일 조건을 조정하세요.</span>
            </div>
          ) : null}
        </div>

        <JobDetail
          isSaved={selectedJob ? savedJobSet.has(selectedJob.id) : false}
          job={selectedJob}
          onToggleSaved={toggleSaved}
        />
      </div>
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Badge({ children }: { children: string }) {
  return <span className="badge">{children}</span>;
}

function JobDetail({
  isSaved,
  job,
  onToggleSaved,
}: {
  isSaved: boolean;
  job: Job | null;
  onToggleSaved: (jobId: string) => void;
}) {
  if (!job) {
    return (
      <aside className="job-detail empty-detail" aria-label="공고 상세">
        <strong>선택된 공고가 없습니다.</strong>
      </aside>
    );
  }

  return (
    <aside className="job-detail" aria-label="공고 상세">
      <div className="detail-header">
        <div>
          <p className="eyebrow">{job.company}</p>
          <h2>{job.title}</h2>
        </div>
        <button className="save-button" onClick={() => onToggleSaved(job.id)} type="button">
          {isSaved ? "저장됨" : "저장"}
        </button>
      </div>

      <p className="detail-summary">{job.summary}</p>

      <div className="detail-tags">
        {job.job_keywords.map((keyword) => (
          <Badge key={keyword}>{keyword}</Badge>
        ))}
      </div>

      <dl className="detail-list">
        <div>
          <dt>지역</dt>
          <dd>{job.location}</dd>
        </div>
        <div>
          <dt>고용형태</dt>
          <dd>{employmentLabels[job.employment_type] ?? job.employment_type}</dd>
        </div>
        <div>
          <dt>마감일</dt>
          <dd>{formatDeadline(job.deadline)}</dd>
        </div>
        <div>
          <dt>출처</dt>
          <dd>{job.source_name}</dd>
        </div>
        <div>
          <dt>수집 시각</dt>
          <dd>{formatDateTime(job.collected_at)}</dd>
        </div>
        <div>
          <dt>원문 확인</dt>
          <dd>{formatDateTime(job.verified_at)}</dd>
        </div>
      </dl>

      <a className="source-link" href={job.source_url} rel="noreferrer" target="_blank">
        원문 열기
      </a>
    </aside>
  );
}

function formatDeadline(deadline: string | null) {
  if (!deadline) {
    return "마감 미정";
  }
  return new Intl.DateTimeFormat("ko-KR", {
    month: "short",
    day: "numeric",
  }).format(new Date(`${deadline}T00:00:00+09:00`));
}

function formatDateTime(value: string) {
  return new Intl.DateTimeFormat("ko-KR", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}
