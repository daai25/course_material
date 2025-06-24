## Part 4: Running Your Pipeline!
You are now ready to run your entire pipeline.

### Step 1: Run the Luigi Pipeline
Open your terminal in the project's root directory and run:

```bash
luigi --module main NewsScrapingPipeline --local-scheduler
```
You will see Luigi check the dependencies and run the Extract, Load, and Analyze tasks in order.

### Step 2: Re-run the Pipeline
Run the same command again a few minutes later. You will see it run again! This is because the DateMinuteParameter creates a new, unique target each time, allowing you to fetch fresh data.

Congratulations! You have successfully built and run a complete, automated data pipeline.

Let us continue with [the last part](./tutorial-part05.md).
