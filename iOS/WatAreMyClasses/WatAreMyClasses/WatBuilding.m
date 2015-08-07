//
//  WatBuilding.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "WatBuilding.h"

@implementation WatBuilding
+ (NSDictionary *)JSONKeyPathsByPropertyKey {
    // properties defined in header < : > key in JSON Dictionary
    return @{
             @"bid": @"id",
             @"name":  @"name",
             };
}
@end
