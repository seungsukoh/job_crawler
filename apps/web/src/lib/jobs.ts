import sampleJobs from "@/fixtures/sample-jobs.json";

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

const staticJobs = sampleJobs as Job[];

const employmentSearchTerms: Record<string, string[]> = {
  conversion_intern: ["conversion intern", "intern", "conversion", "채용연계형", "인턴"],
  entry_level: ["entry level", "entry", "junior", "신입"],
  intern: ["intern", "internship", "인턴"],
  part_time: ["part time", "student", "assistant", "파트타임", "아르바이트", "학생"],
};

const statusSearchTerms: Record<JobStatus, string[]> = {
  active: ["active", "open", "진행", "모집"],
  closed: ["closed", "expired", "마감"],
  deadline_unknown: ["deadline unknown", "rolling", "마감 미정", "상시"],
};

const keywordSearchTerms: Record<string, string[]> = {
  analytics: ["analytics", "analysis", "분석"],
  android: ["android", "안드로이드"],
  automation: ["automation", "자동화"],
  backend: ["backend", "back-end", "server", "api", "백엔드", "서버", "개발", "개발자"],
  cloud: ["cloud", "클라우드"],
  data: ["data", "데이터"],
  devops: ["devops", "operations", "운영"],
  excel: ["excel", "엑셀"],
  fastapi: ["fastapi", "api"],
  frontend: ["frontend", "front-end", "react", "프론트엔드", "프론트", "리액트", "개발", "개발자"],
  kotlin: ["kotlin", "코틀린"],
  linux: ["linux", "리눅스"],
  marketing: ["marketing", "마케팅"],
  mobile: ["mobile", "app", "android", "모바일", "앱", "개발", "개발자"],
  planning: ["planning", "strategy", "기획"],
  product: ["product", "pm", "프로덕트", "기획"],
  python: ["python", "파이썬"],
  qa: ["qa", "quality", "testing", "테스트", "품질"],
  react: ["react", "리액트", "프론트엔드"],
  research: ["research", "리서치", "조사"],
  security: ["security", "보안"],
  sql: ["sql", "database", "db", "데이터베이스"],
  survey: ["survey", "설문"],
  testing: ["testing", "test", "테스트"],
  typescript: ["typescript", "ts", "타입스크립트"],
  ux: ["ux", "user experience", "사용자경험"],
};

export function listStaticJobs(query: JobQuery): JobsResponse {
  let items = staticJobs;

  if (!query.includeClosed) {
    items = items.filter((job) => job.status !== "closed");
  }

  if (query.keyword?.trim()) {
    const normalizedKeyword = normalizeSearchValue(query.keyword);
    items = items.filter((job) => matchesStaticKeyword(job, normalizedKeyword));
  }

  if (query.deadlineFrom || query.deadlineTo) {
    items = items.filter((job) =>
      isWithinDeadlineRange(job.deadline, query.deadlineFrom, query.deadlineTo),
    );
  }

  return {
    items,
    count: items.length,
    filters: {
      keyword: query.keyword?.trim() || null,
      deadline_from: query.deadlineFrom || null,
      deadline_to: query.deadlineTo || null,
      include_closed: Boolean(query.includeClosed),
    },
    data_source: "sample-static",
  };
}

function matchesStaticKeyword(job: Job, normalizedKeyword: string) {
  const searchableValues = [
    job.title,
    job.company,
    job.location,
    job.employment_type,
    job.summary,
    job.status,
    ...job.job_keywords,
    ...job.eligibility_tags,
    ...(employmentSearchTerms[job.employment_type] ?? []),
    ...statusSearchTerms[job.status],
    ...job.job_keywords.flatMap((keyword) => keywordSearchTerms[keyword] ?? []),
  ];

  return searchableValues.some((value) => normalizeSearchValue(value).includes(normalizedKeyword));
}

function isWithinDeadlineRange(
  deadline: string | null,
  deadlineFrom: string | undefined,
  deadlineTo: string | undefined,
) {
  if (!deadline) {
    return false;
  }

  if (deadlineFrom && deadline < deadlineFrom) {
    return false;
  }

  if (deadlineTo && deadline > deadlineTo) {
    return false;
  }

  return true;
}

function normalizeSearchValue(value: string) {
  return value.trim().toLocaleLowerCase("ko-KR");
}
