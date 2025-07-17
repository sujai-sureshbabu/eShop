using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using OrderService;
using OrderService.Services;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using OpenTelemetry.Extensions.Hosting;
using Microsoft.EntityFrameworkCore;




Host.CreateDefaultBuilder(args)
    .ConfigureServices((hostContext, services) =>
    {
        services.Configure<KafkaSettings>(hostContext.Configuration.GetSection("Kafka"));
        services.AddHostedService<KafkaConsumerService>();
        services.AddDbContext<OrderDbContext>(options =>
        {
            options.UseNpgsql(hostContext.Configuration.GetConnectionString("OrderDb"));
        });
        // services.AddOpenTelemetryTracing(builder =>
        // {
        //     builder
        //         .SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("OrderService"))
        //         .AddAspNetCoreInstrumentation()
        //         .AddJaegerExporter(o =>
        //         {
        //             o.AgentHost = hostContext.Configuration["Jaeger:Host"];
        //             o.AgentPort = int.Parse(hostContext.Configuration["Jaeger:Port"]);
        //         });
        // });

    })
    .Build()
    .Run();
