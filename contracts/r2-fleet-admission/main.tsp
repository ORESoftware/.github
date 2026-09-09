namespace Ores.R2Fleet;

enum AdmissionState {
  planned: "planned",
  inProgress: "in_progress",
  blocked: "blocked",
  verified: "verified",
  notApplicable: "not_applicable",
}

enum EvidenceState {
  unknownState: "unknown",
  notExecuted: "not_executed",
  stale: "stale",
  stoppedForEvaluation: "stopped_for_evaluation",
  failed: "failed",
  passed: "passed",
}

enum TaskCategory {
  inventoryState: "inventory_state",
  credentials: "credentials",
  ci: "ci",
  contracts: "contracts",
  migration: "migration",
  lifecycle: "lifecycle",
  application: "application",
  isolation: "isolation",
  crypto: "crypto",
  retention: "retention",
  observability: "observability",
  recovery: "recovery",
}

enum GeneratedEvidenceRole {
  comparisonEvidenceOnly: "comparison_evidence_only",
}

enum AuthorityPrecedence {
  none: "none",
}

model R2AdmissionTask {
  code: string;
  issue: string;
  title: string;
  category: TaskCategory;
  state: AdmissionState;
  dependsOn: string[];
}

model R2OrganizationAdmission {
  organization: string;
  namespaceState: AdmissionState;
  liveInventory: EvidenceState;
  stateOwnership: EvidenceState;
  credentialScope: EvidenceState;
  readIsolation: EvidenceState;
  writeIsolation: EvidenceState;
  applicationAuthorization: EvidenceState;
  keyRecovery: EvidenceState;
  retention: EvidenceState;
  recovery: EvidenceState;
  documentAdmission: AdmissionState;
}

model R2FleetAdmissionProgram {
  schemaVersion: "ores.r2-fleet-admission/v1";
  linearIssue: "DEN-3109";
  githubProgramIssue: string;
  programState: AdmissionState;
  generatedEvidenceRole: GeneratedEvidenceRole;
  authorityPrecedence: AuthorityPrecedence;
  tasks: R2AdmissionTask[];
  organizations: R2OrganizationAdmission[];
}
