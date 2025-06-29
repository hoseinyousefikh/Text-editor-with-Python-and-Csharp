using App.Domain.Core.Home.Contract.Mapper;
using App.Domain.Core.Home.Contract.Repositories;
using App.Domain.Core.Home.DTO;
using App.Domain.Core.Home.Entities;
using App.Infra.Data.Db.SqlServer.Ef.Home.DataDBContaxt;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Infra.Data.Repos.Ef.Home.Repository
{
    public class TextRepository : ITextRepository
    {
        private readonly AppDbContext _context;
        private readonly IHomeMapper _mapper; // افزودن وابستگی به مپر

        public TextRepository(AppDbContext context, IHomeMapper mapper)
        {
            _context = context;
            _mapper = mapper;
        }

        public async Task<UserTextDTO> AddAsync(UserTextDTO dto)
        {
            // تبدیل DTO به Entity
            var entity = _mapper.MapToEntity(dto, dto.UserId);

            _context.UserTexts.Add(entity);
            await _context.SaveChangesAsync();

            // تبدیل Entity برگشتی به DTO
            return _mapper.MapToDto(entity);
        }

        public async Task<IEnumerable<UserTextDTO>> GetAllAsync()
        {
            var entities = await _context.UserTexts.ToListAsync();

            // تبدیل لیست Entity به لیست DTO
            return entities.Select(_mapper.MapToDto);
        }

        public async Task<IEnumerable<UserTextDTO>> GetByUserIdAsync(int userId)
        {
            var entities = await _context.UserTexts
                .Where(t => t.UserId == userId)
                .ToListAsync();

            return entities.Select(_mapper.MapToDto);
        }
    }
}
