/**
 * Type definitions for SIMS frontend
 */

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: 'pg' | 'supervisor' | 'admin';
  specialty?: string;
  year?: string;
  phone_number?: string;
  registration_number?: string;
  date_joined: string;
  is_active: boolean;
}

export interface Department {
  id: number;
  name: string;
  code: string;
  description: string;
  head?: number;
  head_name?: string;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Batch {
  id: number;
  name: string;
  program: string;
  department: number;
  department_name: string;
  start_date: string;
  end_date: string;
  coordinator?: number;
  coordinator_name?: string;
  capacity: number;
  current_strength: number;
  is_full: boolean;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface StudentProfile {
  id: number;
  user: number;
  user_name: string;
  user_email: string;
  batch: number;
  batch_name: string;
  department_name: string;
  roll_number: string;
  admission_date: string;
  expected_graduation_date?: string;
  actual_graduation_date?: string;
  status: string;
  status_updated_at: string;
  cgpa?: number;
  is_active: boolean;
  duration: number;
  created_at: string;
  updated_at: string;
}

export interface Rotation {
  id: number;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  department?: number;
  hospital?: number;
  supervisor?: number;
  students: number[];
  status: string;
  created_at: string;
  updated_at: string;
}

export interface LogbookEntry {
  id: number;
  student: number;
  rotation?: number;
  date: string;
  case_type: string;
  summary: string;
  verified: boolean;
  verified_by?: number;
  verified_on?: string;
  created_at: string;
  updated_at: string;
}

export interface Exam {
  id: number;
  title: string;
  exam_type: string;
  rotation?: number;
  rotation_name?: string;
  module_name?: string;
  date: string;
  start_time?: string;
  duration_minutes?: number;
  max_marks: number;
  passing_marks: number;
  requires_eligibility: boolean;
  status: string;
  conducted_by?: number;
  conducted_by_name?: string;
  instructions?: string;
  remarks?: string;
  created_at: string;
  updated_at: string;
}

export interface Score {
  id: number;
  exam: number;
  exam_title: string;
  exam_date: string;
  student: number;
  student_name: string;
  student_roll?: string;
  marks_obtained: number;
  percentage: number;
  grade: string;
  is_passing: boolean;
  is_eligible: boolean;
  ineligibility_reason?: string;
  remarks?: string;
  created_at: string;
  updated_at: string;
}

export interface Certificate {
  id: number;
  title: string;
  description: string;
  issue_date: string;
  verified: boolean;
  verified_by?: number;
  verified_on?: string;
  created_at: string;
  updated_at: string;
}

export interface AttendanceRecord {
  id: number;
  user: number;
  session: number;
  status: string;
  check_in_time?: string;
  remarks?: string;
  created_at: string;
  updated_at: string;
}

export interface EligibilitySummary {
  id: number;
  user: number;
  period: string;
  start_date: string;
  end_date: string;
  total_sessions: number;
  attended_sessions: number;
  percentage_present: number;
  is_eligible: boolean;
  threshold_percentage: number;
  remarks?: string;
  generated_at: string;
  updated_at: string;
}
