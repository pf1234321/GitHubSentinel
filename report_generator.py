# report_generator.py
class ReportGenerator:
    def generate_report(self, updates):
        report = 'GitHub Updates Report\n'
        for repo, commits in updates.items():
            report += f'\nRepo: {repo}\n'
            for commit in commits:
                report += f'- {commit['commit']['message']} by {commit['commit']['author']['name']}\n'
        return report
