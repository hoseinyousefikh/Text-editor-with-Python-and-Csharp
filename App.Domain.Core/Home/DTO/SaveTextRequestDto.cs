using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace App.Domain.Core.Home.DTO
{
    public class SaveTextRequestDto
    {
        [Required]
        [MinLength(1)]
        public string Content { get; set; }
    }
}
