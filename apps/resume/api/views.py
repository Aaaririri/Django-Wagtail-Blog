from apps.home.api.static_json import StaticJSONView
from apps.resume.models import ResumePage


class ResumeJSONView(StaticJSONView):
    build_path = "api/resume.json"

    def get_data(self):
        page = ResumePage.objects.live().first()
        if page is None:
            return {}
        return {
            "title": page.title,
            "experiences": [
                {
                    "role": e.role,
                    "company": e.company,
                    "start_date": e.start_date,
                    "end_date": e.end_date,
                    "description": e.description,
                }
                for e in page.experiences.all()
            ],
            "education": [
                {
                    "degree": e.degree,
                    "institution": e.institution,
                    "start_year": e.start_year,
                    "end_year": e.end_year,
                }
                for e in page.education_entries.all()
            ],
            "skills": [{"name": s.name, "category": s.category} for s in page.skills.all()],
        }
