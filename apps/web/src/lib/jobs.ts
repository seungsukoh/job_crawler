export type JobStatus = "active" | "closed" | "deadline_unknown";

export type Job = {
  id: string;
  external_id: string;
  title: string;
  company: string;
  job_keywords: string[];
  location: string;
  employment_type: string;
  eligibility_tags: string[];
  deadline: string | null;
  status: JobStatus;
  source_name: string;
  source_url: string;
  collected_at: string;
  verified_at: string;
  summary: string;
  is_sample: boolean;
};

export type JobsResponse = {
  items: Job[];
  count: number;
  filters: {
    keyword: string | null;
    deadline_from: string | null;
    deadline_to: string | null;
    include_closed: boolean;
  };
  data_source: "sample" | "database" | string;
};

export type JobQuery = {
  keyword?: string;
  deadlineFrom?: string;
  deadlineTo?: string;
  includeClosed?: boolean;
};

export function buildJobsUrl(apiBaseUrl: string, query: JobQuery) {
  const url = new URL(`${apiBaseUrl.replace(/\/$/, "")}/jobs`);

  if (query.keyword?.trim()) {
    url.searchParams.set("keyword", query.keyword.trim());
  }

  if (query.deadlineFrom) {
    url.searchParams.set("deadline_from", query.deadlineFrom);
  }

  if (query.deadlineTo) {
    url.searchParams.set("deadline_to", query.deadlineTo);
  }

  if (query.includeClosed) {
    url.searchParams.set("include_closed", "true");
  }

  return url.toString();
}
