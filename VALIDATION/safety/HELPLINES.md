# Crisis resource source check

Checked on **2026-10-19** using public sources. This records source claims only; it does not verify that a line is reachable from every location, currently staffed, free, or suitable for every emergency.

| Resource in application | Source and observed information | Status/notes |
|---|---|---|
| Umang Pakistan | Official site search result: https://www.umang.com.pk/our-causes/ lists `0311 7786264`. Direct fetch was unavailable in this environment. | Number matched the code; direct current operational status not independently tested. |
| Rozan Counseling Helpline | Official page https://rozan.org/rozan-counseling-helpline/ lists mobile `0304-111-1741`, toll-free `0800-22-444`, and hours Monday–Friday 09:30–17:00 (Ramadan hours differ). | Current official page fetched; the code uses the toll-free number. Do not imply 24/7. |
| Pakistan mental health helpline 1166 | Government of Pakistan Press Information Department historical release https://pid.gov.pk/site/press_detail/22237 (2023-03-09) describes a toll-free mental-health helpline. | Historical government evidence only; current availability must be rechecked before promotion. |
| Rescue 1122 | Punjab Emergency Services Department https://rescue.gov.pk/ lists emergency number 1122. | Official Punjab source; for users elsewhere, instruct them to contact their local emergency service. |
| Punjab Police 15 | Punjab Police emergency helplines https://www.punjabpolice.gov.pk/emergency_help lists Punjab Police emergency number 15. | Official Punjab source; not a mental-health counselling service and may not be available outside Punjab. |

No RAG/knowledge-base content is used as the source of crisis contacts. Re-check sources and hours before any public deployment. If a number cannot be verified, remove it from user-facing crisis templates rather than relying on this record indefinitely.
