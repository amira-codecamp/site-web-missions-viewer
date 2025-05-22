
export interface Status {
  status_name: string;
}

export interface EmployeeWithStatus {
  first_name: string;
  last_name: string;
  email: string;
  status: Status;
}

export interface Employee {
  first_name: string;
  last_name: string;
  email: string;
}