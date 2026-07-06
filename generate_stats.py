import json
import subprocess
import sys

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        print(f"Error running command {cmd}: {e}")
        return None

# Fetch Commits
commits_str = run_cmd(["gh", "api", "/search/commits?q=author:DakshMehrotra", "--jq", ".total_count", "--header", "Accept: application/vnd.github.cloak-preview"])
commits = int(commits_str) if commits_str else 1315

# Fetch PRs
prs_str = run_cmd(["gh", "api", "/search/issues?q=author:DakshMehrotra+type:pr", "--jq", ".total_count"])
prs = int(prs_str) if prs_str else 41

# Fetch Repos Count & Created Date
graphql_query = 'query { user(login: "DakshMehrotra") { createdAt repositories(ownerAffiliations: OWNER) { totalCount } } }'
user_data_str = run_cmd(["gh", "api", "graphql", "-f", f"query={graphql_query}"])

repos = 53
active_since = "Oct 2023"

if user_data_str:
    try:
        user_data = json.loads(user_data_str)
        user = user_data["data"]["user"]
        repos = user["repositories"]["totalCount"]
        created_at = user["createdAt"] # format: "2023-10-24T10:17:02Z"
        year = created_at.split("-")[0]
        month_num = created_at.split("-")[1]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month = months[int(month_num) - 1]
        active_since = f"{month} {year}"
    except Exception as e:
        print(f"Error parsing graphql user data: {e}")

# Build SVG
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 140" width="850" height="140">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020205" />
      <stop offset="50%" stop-color="#050614" />
      <stop offset="100%" stop-color="#08091a" />
    </linearGradient>

    <!-- Glowing Filters -->
    <filter id="greenGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="blueGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Grid Pattern -->
    <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
      <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#00d4ff" stroke-width="0.75" stroke-opacity="0.03" />
    </pattern>

    <style>
      .header-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 800;
        font-size: 11px;
        fill: #64748b;
        letter-spacing: 2px;
      }}

      .metric-label {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 500;
        font-size: 13px;
        fill: #94a3b8;
        letter-spacing: 1px;
      }}

      .metric-value {{
        font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
        font-weight: 700;
        font-size: 18px;
        letter-spacing: 1px;
      }}

      .green-val {{ fill: #00ff88; filter: url(#greenGlow); }}
      .blue-val {{ fill: #00d4ff; filter: url(#blueGlow); }}
      .purple-val {{ fill: #a78bfa; }}
      .white-val {{ fill: #ffffff; }}
    </style>
  </defs>

  <!-- Background -->
  <rect width="850" height="140" fill="url(#bgGrad)" rx="8" stroke="#1e293b" stroke-width="1.5" />
  <rect width="850" height="140" fill="url(#grid)" rx="8" />

  <!-- LEFT PANEL: Core Github Metrics -->
  <g transform="translate(45, 30)">
    <text x="0" y="10" class="header-title">GITHUB CORE METRICS</text>
    
    <!-- Commits -->
    <g transform="translate(0, 35)">
      <text x="0" y="15" class="metric-label">Total Commits</text>
      <text x="180" y="16" class="metric-value green-val">{commits}</text>
    </g>

    <!-- Pull Requests -->
    <g transform="translate(0, 65)">
      <text x="0" y="15" class="metric-label">Pull Requests</text>
      <text x="180" y="16" class="metric-value blue-val">{prs}</text>
    </g>
  </g>

  <!-- Vertical Divider -->
  <line x1="425" y1="20" x2="425" y2="120" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4" />

  <!-- RIGHT PANEL: Node Diagnostics -->
  <g transform="translate(470, 30)">
    <text x="0" y="10" class="header-title">SYSTEM DIAGNOSTICS</text>

    <!-- Repositories -->
    <g transform="translate(0, 35)">
      <text x="0" y="15" class="metric-label">Total Repositories</text>
      <text x="200" y="16" class="metric-value purple-val">{repos}</text>
    </g>

    <!-- Active Since / Integrity -->
    <g transform="translate(0, 65)">
      <text x="0" y="15" class="metric-label">Operational Since</text>
      <text x="200" y="16" class="metric-value white-val">{active_since}</text>
    </g>
  </g>
</svg>
"""

with open("stats.svg", "w") as f:
    f.write(svg_content)

print("✓ stats.svg generated successfully.")
