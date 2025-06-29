using App.Domain.Core.Home.Contract.Mapper;
using App.Domain.Core.Home.DTO;
using App.Domain.Core.Home.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Infra.Data.Repos.Ef.Home.Mapper
{
    public class HomeMapper : IHomeMapper
    {
       

       

        public UserTextDTO MapToDto(UserText entity)
        {
            return new UserTextDTO
            {
                TextId = entity.TextId,
                Content = entity.Content,
                CreatedAt = entity.CreatedAt,
                UpdatedAt = entity.UpdatedAt,
                UserId = entity.UserId
            };
        }

        public UserText MapToEntity(UserTextDTO dto, int userId)
        {
            return new UserText
            {
                TextId = dto.TextId,
                Content = dto.Content,
                CreatedAt = dto.CreatedAt,
                UpdatedAt = dto.UpdatedAt,
                UserId = userId
            };
        }
    }
}
