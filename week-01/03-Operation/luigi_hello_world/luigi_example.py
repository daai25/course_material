import luigi

# TASK 1: Create a file with "Hello"
class HelloTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget('hello.txt')

    def run(self):
        # The 'with' statement ensures the file is properly closed
        with self.output().open('w') as f:
            f.write('Hello')

# TASK 2: Depends on HelloTask, adds "World"
class WorldTask(luigi.Task):
    def requires(self):
        return HelloTask() # This task requires HelloTask to be complete

    def output(self):
        return luigi.LocalTarget('world.txt')

    def run(self):
        # self.input() refers to the output of the required task
        with self.input().open('r') as infile, self.output().open('w') as outfile:
            outfile.write(infile.read() + ' World!')

