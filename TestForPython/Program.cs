using App.Domain.AppServices.Home.AppServices;
using App.Domain.Core.Home.Contract.AppServices;
using App.Domain.Core.Home.Contract.Mapper;
using App.Domain.Core.Home.Contract.Repositories;
using App.Domain.Core.Home.Contract.Services;
using App.Domain.Services.Home.Services;
using App.Infra.Data.Db.SqlServer.Ef.Home.DataDBContaxt;
using App.Infra.Data.Repos.Ef.Home.Mapper;
using App.Infra.Data.Repos.Ef.Home.Repository;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System;
using System.Text;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));
// Add services to the container.
// ثبت لایه‌ها
builder.Services.AddScoped<ITextRepository, TextRepository>();
builder.Services.AddScoped<ITextService, TextService>();
builder.Services.AddScoped<ITextAppService, TextAppService>();
// اضافه کردن Mapper به سرویس‌ها
builder.Services.AddScoped<IHomeMapper, HomeMapper>();
builder.Services.AddScoped<AppDbContext>();

// ثبت DbContext

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = false,
            ValidateAudience = false,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Secret"]))
        };
    });
builder.Services.AddControllers();
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
builder.Services.AddSwaggerGen();
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", builder =>
    {
        builder.AllowAnyOrigin()
               .AllowAnyMethod()
               .AllowAnyHeader();
    });
});
var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowAll");
app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.Run();
