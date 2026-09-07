namespace Ores.Governance;

/** Observation state for a repository or external organization mapping. */
enum ResourceStatus {
  verified,
  declared,
  drift,
  missing,
  blocked,
  unverified,
}

/** Visibility relevant to governance checks. */
enum RepositoryVisibility {
  public,
  private,
  internal,
  unknown,
}

/** Canonical repository roles used by organization alignment. */
enum RepositoryRole {
  canonical,
  documentation,
  marketing,
  mcpServer,
  cli,
  interfaces,
  clients,
  monorepo,
  infrastructure,
  desktopRust,
  flutter,
  lambdas,
  apiServer,
  adminApiServer,
  webServer,
  adminWebServer,
  libCore,
  ormCore,
  pubLibCore,
  sync,
  other,
}

/** External resource types in the organization-to-provider mapping. */
enum MappingKind {
  linearProject,
  githubProject,
  supabaseOrganization,
  supabaseNamespace,
  neonOrganization,
  cloudflareDomain,
  gcpProject,
  slackChannel,
}

/** One repository surface and its last authoritative observation. */
model RepositorySurface {
  role: RepositoryRole;
  /** Owner-qualified repository name. */
  repository: string;
  required: boolean;
  status: ResourceStatus;
  expectedVisibility?: RepositoryVisibility;
  observedVisibility?: RepositoryVisibility;
  /** Canonical or mirror manifest path used by this repository. */
  manifestPath?: string;
  /** `full`, `pointer`, or `none`. */
  mirrorMode?: string;
  /** Human-readable evidence reference without secret material. */
  evidence?: string;
}

/** One external provider/project/channel mapping. */
model ExternalMapping {
  kind: MappingKind;
  /** Public or non-secret identifier. Omit while genuinely unknown. */
  identifier?: string;
  status: ResourceStatus;
  evidence?: string;
  note?: string;
}

/** Append-only explanation of a direction change. */
model Supersession {
  sequence: int32;
  recordedAt: string;
  formerStatement: string;
  replacementStatement: string;
  reason: string;
  evidence: string;
}

/** Canonical organization source-of-truth manifest. */
model OrganizationSourceOfTruth {
  schemaVersion: string;
  revision: int32;
  organization: string;
  authorityRepository: string;
  canonicalPath: string;
  /** Must remain `append-only`. */
  synchronizationPolicy: string;
  reviewedAt: string;
  linearIssue?: string;
  githubIssue?: string;
  repositories: RepositorySurface[];
  mappings: ExternalMapping[];
  supersessions: Supersession[];
}
