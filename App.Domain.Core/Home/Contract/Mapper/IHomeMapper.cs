using App.Domain.Core.Home.DTO;
using App.Domain.Core.Home.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Domain.Core.Home.Contract.Mapper
{
    public interface IHomeMapper
    {
      

        UserTextDTO MapToDto(UserText entity);
        UserText MapToEntity(UserTextDTO dto, int userId);
    }
}
