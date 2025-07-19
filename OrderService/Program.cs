using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using OrderService;
using OrderService.Services;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Extensions.Hosting;
using Microsoft.EntityFrameworkCore;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((hostContext, services) =>
    {
        services.Configure<KafkaSettings>(hostContext.Configuration.GetSection("Kafka"));
        services.AddHostedService<KafkaConsumerService>();
        services.AddDbContext<OrderDbContext>(options =>
        {
            options.UseNpgsql(hostContext.Configuration.GetConnectionString("OrderDb"));
        });
        services.AddOpenTelemetry()
            .WithTracing(tracing =>
            {
                tracing
                    .SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("OrderService"))
                    .AddAspNetCoreInstrumentation()
                    .AddJaegerExporter(o =>
                    {
                        o.AgentHost = hostContext.Configuration["Jaeger:Host"];
                        o.AgentPort = int.Parse(hostContext.Configuration["Jaeger:Port"]);
                    });
            });
    })
    .Build();

// Run migrations here before starting the host
using var scope = host.Services.CreateScope();
var db = scope.ServiceProvider.GetRequiredService<OrderDbContext>();

var retries = 10;
var delay = TimeSpan.FromSeconds(5);

while (retries > 0)
{
    try
    {
        db.Database.Migrate();
        break; // Success, exit loop
    }
    catch (Exception ex)
    {
        retries--;
        Console.WriteLine($"Failed to connect to DB. Retries left: {retries}. Exception: {ex.Message}");
        if (retries == 0) throw; // Give up
        Thread.Sleep(delay);
    }
}

host.Run();

