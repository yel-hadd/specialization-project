export interface Kpis {
  n_students: number;
  n_grades: number;
  overall_average: number | null;
  success_rate: number | null;
  absence_rate: number | null;
  n_at_risk: number;
  progression: number | null;
}

export interface AnomalyReport {
  grade_outliers: {
    student_id: number;
    student_code: string;
    module_name: string;
    value: number;
    module_mean: number;
    z_score: number;
  }[];
  absence_outliers: {
    student_id: number;
    student_code: string;
    absence_hours: number;
  }[];
}

export interface ModuleStat {
  module_id: number;
  module_code: string;
  module_name: string;
  mean: number;
  median: number;
  min: number;
  max: number;
  variance: number;
  std: number;
  q1: number;
  q3: number;
  success_rate: number;
  fail_rate: number;
}

export interface ClassStat {
  class_id: number;
  class_name: string;
  mean: number;
  std: number;
  success_rate: number;
  n_students: number;
}

export interface Distribution {
  edges: string[];
  counts: number[];
}

export interface CorrelationMatrix {
  labels: string[];
  matrix: number[][];
}

export interface AtRiskStudent {
  student_id: number;
  student_code: string;
  name: string;
  class_name: string | null;
  average: number;
  absence_rate: number;
  risk_score: number;
  segment: string;
  recommendations: string[];
}

export interface Alert {
  id: number;
  student_id: number;
  alert_type: string;
  severity: string;
  message: string;
  threshold_value: number | null;
  metric_value: number | null;
  created_at: string;
  resolved: boolean;
}

export interface ImportLog {
  id: number;
  filename: string;
  type: string;
  imported_at: string;
  rows_processed: number;
  rows_rejected: number;
  status: string;
  error_log: string | null;
}

export interface Student {
  id: number;
  student_code: string;
  first_name: string;
  last_name: string;
  email: string | null;
  class_id: number | null;
}

export interface StudentDetail {
  student: Student;
  class_name: string | null;
  average: number | null;
  absence_hours: number;
  absence_rate: number;
  rank: number | null;
  class_size: number | null;
  risk_segment: string;
  grades: { id: number; module_id: number; value: number; period: string | null }[];
  absences: { id: number; hours: number; type: string; justified: boolean }[];
  progression: { period: string; average: number }[];
  recommendations: string[];
}

