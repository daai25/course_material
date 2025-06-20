import luigi
from analyse.tasks import AnalyzeData
from datetime import datetime

class NewsScrapingPipeline(luigi.WrapperTask):
    """Main pipeline orchestrator: triggers the full ETL chain."""

    run_time = luigi.DateMinuteParameter(default=datetime.now())

    def requires(self):
        return AnalyzeData(run_time=self.run_time)

if __name__ == '__main__':
    luigi.run()
